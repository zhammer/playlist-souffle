"""AWS lambda function for shuffling a playlist's tracks by artist or album.

TODO: Cleanup delivery functions.
"""

import logging
from urllib.parse import parse_qs
from playlist_souffle.definitions.exception import SouffleParameterError, SouffleSpotifyError
from playlist_souffle.gateways.spotify import SpotifyGateway
from playlist_souffle.use_cases.souffle_playlist import souffle_playlist
from playlist_souffle.delivery.aws_lambda.util import (
    extract_bearer_token_from_api_event,
    generate_api_gateway_response
)

logger = logging.getLogger(__name__)

def generate_spotify_exception_response(exception):
    """Generate an api gateway response based on a spotify exception."""
    if exception.http_status == 401:
        return generate_api_gateway_response(401, body={'message': exception.message})
    else:
        return generate_api_gateway_response(
            500,
            body={
                'message':'Encountered Spotify api error. Message: "{}".'.format(exception.message)
            }
        )


def handler(event, context):
    """AWS lambda event handler"""

    logger.debug('Handling event "%s". Context: "%s"', event, context)

    # Get access token
    try:
        access_token = extract_bearer_token_from_api_event(event)
    except LookupError as e:
        return generate_api_gateway_response(
            400,
            body={'message':str(e)}
        )

    # Extract request body
    request_body = parse_qs(event['body'])

    # Required fields
    try:
        playlist_uri = request_body['playlistUri'][0]
        shuffle_by = request_body['shuffleBy'][0]
    except KeyError as e:
        return generate_api_gateway_response(
            400,
            body={'message':'Missing field: "{}".'.format(e)}
        )

    # Setup spotipy client
    try:
        spotify = SpotifyGateway(access_token)
    except SouffleSpotifyError as e:
        return generate_spotify_exception_response(e)


    # Souffle playlist
    try:
        souffled_playlist_uri = souffle_playlist(spotify, playlist_uri, shuffle_by)
    except SouffleParameterError as e:
        return generate_api_gateway_response(400, body={'message': e})
    except SouffleSpotifyError as e:
        return generate_spotify_exception_response(e)
    # except Exception as e:
    #     logger.error('Unexpected exception: "{}".'.format(e))
    #     return generate_api_gateway_response(500)

    # Return success
    headers = {
        'Location': souffled_playlist_uri,
        'Access-Control-Allow-Origin': 'https://playlistsouffle.com',
        'Access-Control-Allow-Credentials': True,
        'Access-Control-Expose-Headers': 'location'
    }
    return generate_api_gateway_response(201, headers=headers)
