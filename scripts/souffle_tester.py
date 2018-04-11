#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
import requests

SOUFFLE_ENDPOINT_URL = 'https://wumxvuo5nb.execute-api.us-east-1.amazonaws.com/dev/souffle'
SOUFFLE_LOCAL_CMD_FMT = 'sls invoke local -f souffle-playlist -p {} --log'

def _parse_args():
    """Helper function to create the command-line argument parser for souffle-tester.  Return
    the parsed arguments as a Namespace object if successful. Exits the program if unsuccessful
    or if the help message is printed.
    """
    description = ('Souffle a playlist using the /souffle endpoint or a local lambda invocation')
    epilog = ('Send a POST request to the /souffle endpoint to souffle a playlist. If the --local\n'
              'flag is set, process the request via a local lambda invocation. On success, the \n'
              'newly created playlist\'s uri is printed to stdout. Otherwise, an error message printed\n'
              'to stderr.\n\n'
              '* Obtaining a spotify accesstoken *\n'
              '1. Visit "https://accounts.spotify.com/authorize?client_id=b231329aba1a4c539375436a2'
              '67db917&response_type=code&redirect_uri=https://127.0.0.1:8100&scope=playlist-modify-public"\n'
              '2. Enter your spotify username and password to grant playlist-modify-public scope.\n'
              '3. Copy the authorization code returned as a url parameter: "/?code={AUTHORIZATION_CODE}"\n'
              '   - Auth redirection will error, but the auth code can still be extracted from the url.\n'
              '4. Use the scripts/refreshtoken.sh script to obtain a refresh token and access token\n'
              '5. If your access token expires, use the scripts/accesstoken.sh script to obtain a fresh '
              'access token.')
    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-a', '--access-token',
                        required=True,
		        help='Spotify access token. See -h for access token instructions.')


    parser.add_argument('-l', '--local',
                        required=False,
                        action='store_true',
		        help='If set, process the souffle request via a local lambda invocation.')

    parser.add_argument('-p', '--playlist-uri',
                        required=True,
		        help='Uri of the playlist to be souffled. Original playlist will not be altered.')

    parser.add_argument('-s', '--shuffle-by',
                        required=True,
		        help='Collection type to shuffle by.',
                        choices=['artist', 'album'])

    parser.add_argument('-u', '--user-id',
                        required=True,
		        help='User id of account where souffled playlist will be created.')

    return parser.parse_args()


def souffle_invoke_local(access_token, **kwargs):
    """Invoke the souffle function as a local lambda via serverless CLI."""

    with tempfile.NamedTemporaryFile(buffering=0) as temp:
        event = {
            'headers': {
                'Authorization': 'Bearer {}'.format(access_token)
            },
            'body': urllib.parse.urlencode(kwargs)
        }

        event_json = json.dumps(event).encode()
        temp.write(event_json)

        local_souffle_command = SOUFFLE_LOCAL_CMD_FMT.format(temp.name)

        process = subprocess.Popen(
            local_souffle_command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        out, err = process.communicate()

        if process.returncode:
            raise RuntimeError(err)

        response = json.loads(out)
        if not response['statusCode'] == requests.codes.created:
            raise RuntimeError('{} response from /souffle endpoint. text: "{}"'.format(
                response['statusCode'], json.loads(response['body'])['message']
            ))

        return response['headers']['Location']


def souffle_invoke_http(access_token, **kwargs):
    """Invoke the souffle function as an http request to the /souffle endpoint."""
    payload = kwargs
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.post(
        SOUFFLE_ENDPOINT_URL,
        headers=headers,
        data=payload
    )

    if not response.status_code == requests.codes.created:
        raise RuntimeError('{} response from /souffle endpoint. text: "{}"'.format(
            response.status_code, response.text
        ))

    return response.headers['Location']


def main():
    """Main"""
    args = _parse_args()

    invoke_function = souffle_invoke_local if args.local else souffle_invoke_http

    try:
        souffled_playlist_uri = invoke_function(
            args.access_token,
            playlistUri=args.playlist_uri,
            shuffleBy=args.shuffle_by,
            userId=args.user_id
        )
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1

    print('Souffled playlist: "{}"'.format(souffled_playlist_uri))


if __name__ == '__main__':
    main()
