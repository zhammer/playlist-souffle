"""AWS lambda function for obtaining a spotify access token given a spotify refresh token."""

import logging
import os
import requests
from souffle.util import (
    decrypt_kms_string,
    extract_bearer_token_from_api_event,
    generate_api_gateway_response
    )


SPOTIFY_ACCESS_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
GRANT_TYPE = 'refresh_token'

logger = logging.getLogger(__name__)


def fetch_spotify_access_token(refresh_token, client_id, client_secret):
    """Fetch an access token from the spotify API given an refresh token.
    Returns None if an access token cannot be obtained given the provided refresh token.

    (For more information, read the Spotify Authorization Code Flow.)

    Args:
        refresh_token: String of refresh token from the spotify API
        client_id: String of spotify client id
        client_secret: String of spotify client secret

    Returns:
        String of fetched access token if successful, otherwise None

    """
    payload = {'grant_type': GRANT_TYPE,
               'refresh_token': refresh_token}

    response = requests.post(
        SPOTIFY_ACCESS_TOKEN_ENDPOINT,
        auth=(client_id, client_secret),
        data=payload
    )

    # If request fails, raise HTTPError
    if not response.status_code == requests.codes.ok:
        logger.info(
            'Failed to retrieve access token for refresh token "***%s". HTTP status: %s.',
            refresh_token[-4:],
            response.status_code
        )
        raise requests.HTTPError()

    # Extract access token and return
    access_token = response.json()['access_token']
    logger.debug(
        'Successfully retrieved access token "***%s" for refresh token "***%s".',
        access_token[-4:],
        refresh_token[-4:]
    )
    return access_token


def main(event, context):
    """AWS lambda event handler"""

    logger.debug('Handling event "%s". Context: "%s"', event, context)

    # Get environment variables
    spotify_client_id = decrypt_kms_string(os.environ['SPOTIFY_CLIENT_ID'])
    spotify_client_secret = decrypt_kms_string(os.environ['SPOTIFY_CLIENT_SECRET'])

    # If event doesn't contain a valid Bearer token, return 400 BAD_REQUEST
    try:
        refresh_token = extract_bearer_token_from_api_event(event)
    except LookupError as e:
        return generate_api_gateway_response(
            400,
            message=str(e)
        )

    # Fetch access token. If token is not obtained, return 401 UNAUTHORIZED.
    try:
        access_token = fetch_spotify_access_token(
            refresh_token,
            spotify_client_id,
            spotify_client_secret
        )
    except requests.HTTPError:
        return generate_api_gateway_response(401)

    # Return access token with 200 OK status code.
    return generate_api_gateway_response(
        200,
        accessToken=access_token
    )
