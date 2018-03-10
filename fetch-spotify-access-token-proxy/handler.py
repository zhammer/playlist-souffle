"""AWS lambda function for obtaining spotify access token given a spotify refresh token via an API
Gateway endpoint request. This handler wraps around the non-HTTP specific fetch-spotify-access-token
lambda function.

Note: Request / Response integration mapping seemed to difficult to implement correctly, though
would reduce the cost from two lambda calls to one.
"""

import json
import logging
import re
import boto3

EXTRACT_BEARER_TOKEN_RE = r'Bearer ([^\s]+)$'
FETCH_SPOTIFY_TOKEN_LAMBDA = 'playlist-souffle-dev-fetch-spotify-access-token'
logger = logging.getLogger(__name__)

# TODO: Move to common module
def extract_bearer_token(string):
    """Extract a bearer token from a Bearer authorization header. Returns None if token is empty
    or if string does not follow Bearer template.

    # Valid bearer token:
    >>> extract_bearer_token('Bearer MY_TOKEN')
    'MY_TOKEN'

    # Empty bearer token:
    >>> extract_bearer_token('Bearer ') is None
    True

    # Invalid bearer token:
    >>> extract_bearer_token('MY_TOKEN') is None
    True

    """
    match = re.match(EXTRACT_BEARER_TOKEN_RE, string)
    if not match:
        logger.debug('Failed to extract bearer token from authorization header: %s', string)
        return None

    return match.group(1)

# TODO: Move to common module
def generate_api_gateway_response(status_code, **body_kwargs):
    """Generate an http response for a lambda API Gateway proxy function with a given status
    code and body.

    Args:
        status_code: Integer of http status code
        body_kwargs: Keyword args used to populate response body JSON

    Returns:
        Dict representation of response

    >>> generate_api_gateway_response(200, message='Success!')
    {'statusCode': 200, 'body': '{"message": "Success!"}'}

    """
    response = {
        'statusCode': status_code
    }
    if body_kwargs:
        response['body'] = json.dumps(body_kwargs)

    return response

# TODO: Move to common module
def fetch_spotify_access_token(refresh_token):
    """Fetch a spotify access token given a refresh token. Returns spotify access token on success,
    otherwise returns None.
ser    """
    lambda_client = boto3.client('lambda')

    payload = {'refreshToken': refresh_token}
    response = lambda_client.invoke(
        FunctionName=FETCH_SPOTIFY_TOKEN_LAMBDA,
        Payload=json.dumps(payload).encode()
    )

    if not response['StatusCode'] == 200:
        logger.warning(
            'Received %d status code from "%s" invocation.',
            response['StatusCode'],
            FETCH_SPOTIFY_TOKEN_LAMBDA
        )
        return None

    access_token = json.loads(response['Payload'].read())
    return access_token


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
