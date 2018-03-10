"""Module for util functions in the playlist souffle service.

Available functions:
- decrypt_kms_string: Decrypt a kms-encrypted string.
- extract_bearer_token: Extract a bearer token from a Bearer auth header.
- fetch_spotify_access_token: Fetch a spotify access token using a refresh token via a lambda call.
- generate_api_gateway_response: Generate an api gateway response with a statuscode and json body.
"""

from base64 import b64decode
import json
import logging
import re
import boto3

EXTRACT_BEARER_TOKEN_RE = r'Bearer ([^\s]+)$'
FETCH_SPOTIFY_TOKEN_LAMBDA = 'playlist-souffle-dev-fetch-spotify-access-token'

logger = logging.getLogger(__name__)


def decrypt_kms_string(encrypted_string):
    """Decrypt string encrypted with the lambda's kms key. Returns the decrypted value on success.
    Raises a RuntimeError if the encrypted string cannot be decoded by kms."""
    kms = boto3.client('kms')
    encrypted_bytes = b64decode(encrypted_string)
    response = kms.decrypt(CiphertextBlob=encrypted_bytes)

    try:
        decrypted_string = response['Plaintext']
    except KeyError:
        raise RuntimeError('Kms decryption for string "{}" failed. Respose: "{}".'.format(
            encrypted_string,
            response
        ))

    return decrypted_string


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


def fetch_spotify_access_token(refresh_token):
    """Fetch a spotify access token given a refresh token. Returns spotify access token on success,
    otherwise returns None.
    Note: This function calls an external lambda function that fetches the access token. This
    funtion does not interact with the spotify api itself.
    """
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
