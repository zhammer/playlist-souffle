"""AWS lambda function for obtaining spotify access token given a spotify refresh token via an API
Gateway endpoint request. This handler wraps around the non-HTTP specific fetch-spotify-access-token
lambda function.

Note: Request / Response integration mapping seemed to difficult to implement correctly, though
would reduce the cost from two lambda calls to one.
"""

import logging
from souffle.util import (
    generate_api_gateway_response,
    extract_bearer_token,
    fetch_spotify_access_token
)

logger = logging.getLogger(__name__)

def main(event, context):
    """AWS lambda event handler"""
    logger.debug('Handling event "%s". Context: "%s"', event, context)

    # If event doesn't contain an Authorization header, send 400 BAD_REQUEST
    try:
        auth_header = event['headers']['Authorization']
    except KeyError:
        logger.debug('Missing "Authorization" header in event %s', event)
        return generate_api_gateway_response(
            400,
            message='Missing "Authorization" header.'
        )

    # If event doesn't contain valid Bearer token, send 400 BAD_REQUEST
    refresh_token = extract_bearer_token(auth_header)
    if not refresh_token:
        return generate_api_gateway_response(
            400,
            message='Invalid Bearer token.'
        )

    # Fetch access token. If token is not obtained, return 401 UNAUTHORIZED.
    access_token = fetch_spotify_access_token(refresh_token)
    if not access_token:
        return generate_api_gateway_response(401)

    # If token is obtained, return access token in 200 OK response.
    return generate_api_gateway_response(
        200,
        accessToken=access_token
    )
