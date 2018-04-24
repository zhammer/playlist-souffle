"""AWS lambda function for obtaining a spotify refresh token (and access token) given a spotify
authorization token.

TODO: Cleanup delivery functions.
"""


import logging
import os
from urllib.parse import parse_qs
import requests
from playlist_souffle.delivery.aws_lambda.util import (
    decrypt_kms_string,
    extract_bearer_token_from_api_event,
    generate_api_gateway_response
)

SPOTIFY_REFRESH_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
GRANT_TYPE = 'authorization_code'

logger = logging.getLogger(__name__)

def fetch_spotify_refresh_token(authorization_token, redirect_uri, client_id, client_secret):
    """Fetch a refresh and access token from the spotify API given an authorization token.
    Raises HTTPError  if an refresh token cannot be obtained given the provided access token.

    (For more information, read the Spotify Authorization Code Flow.)

    Args:
        authorization_token: String of authorization token from the spotify API
        redirect_uri: String of redirect uri used to obtain auth token.
        client_id: String of spotify client id
        client_secret: String of spotify client secret

    Returns:
        Tuple representation of (refresh_token, access_token)

    Raises:
        requests.HTTPError if request to spotify api fails.

    """
    payload = {'grant_type': GRANT_TYPE,
               'code': authorization_token,
               'redirect_uri': redirect_uri}

    response = requests.post(
        SPOTIFY_REFRESH_TOKEN_ENDPOINT,
        auth=(client_id, client_secret),
        data=payload
    )

    # If request fails, raise an HTTPError
    if not response.status_code == requests.codes.ok:
        logger.info(
            'Failed to retrieve refresh token for authorization token "***%s". HTTP status: %s.',
            authorization_token[-4:],
            response.status_code
        )
        raise requests.HTTPError()

    # Extract refresh and access tokens and return as tuple
    response_json = response.json()
    refresh_token = response_json['refresh_token']
    access_token = response_json['access_token']
    logger.debug(
        'Successfully retrieved refresh token "***%s" and access token "***%s" for '
        'authorization token "***%s".',
        refresh_token[-4:],
        access_token[-4:],
        authorization_token[-4:]
    )
    return refresh_token, access_token


def handler(event, context):
    """AWS lambda event handler"""

    logger.debug('Handling event "%s". Context: "%s"', event, context)

    # If event doesn't contain an Authorization header, send 400 BAD_REQUEST
    try:
        authorization_token = extract_bearer_token_from_api_event(event)
    except LookupError as e:
        return generate_api_gateway_response(
            400,
            body={'message':str(e)}
        )

    # If event doesn't contain the redirectUri field, send 400 BAD_REQUEST
    try:
        redirect_uri = parse_qs(event['body'])['redirectUri'][0]
    except KeyError:
        return generate_api_gateway_response(
            400,
            body={'message':'Request must contain a "redirectUri" field'}
        )

    # Get environment variables
    spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
    spotify_client_secret = decrypt_kms_string(os.environ['SPOTIFY_CLIENT_SECRET'])

    # Fetch refresh and access tokens. If tokens are not obtained, returned 401 UNAUTHORIZED.
    try:
        refresh_token, access_token = fetch_spotify_refresh_token(
            authorization_token,
            redirect_uri,
            spotify_client_id,
            spotify_client_secret
        )
    except requests.HTTPError:
        return generate_api_gateway_response(
            401
        )

    # Return refresh and access tokens with 200 OK status code.
    return generate_api_gateway_response(
        200,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        body={
            'refreshToken':refresh_token,
            'accessToken':access_token
        }
    )
