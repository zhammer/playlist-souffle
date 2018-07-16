"""Module containing AWS delivery util functions.

Available functions:
- decrypt_kms_string: Decrypt a kms-encrypted string.
- extract_bearer_token: Extract a bearer token from a Bearer auth header.
- extract_bearer_token_from_api_event: Extract a bearer token from an API Gateway event.
- generate_api_gateway_response: Generate an api gateway response with a statuscode, header and body.
"""

from base64 import b64decode
import functools
import json
import logging
import re
import boto3

EXTRACT_BEARER_TOKEN_RE = r'Bearer ([^\s]+)$'

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
    return match.group(1) if match else None


def extract_bearer_token_from_api_event(event):
    """Extracts a bearer token from an api gateway event. Returns the api token on success.
    Raises a LookupError If the Authorization header is missing, or if the Authorization header
    does not contain a valid Bearer token."""
    try:
        auth_header = event['headers']['Authorization']
    except (KeyError, TypeError):
        logger.debug('Missing "Authorization" header in event %s.', event)
        raise LookupError('Missing "Authorization" header.')

    bearer_token = extract_bearer_token(auth_header)
    if not bearer_token:
        logger.debug('Failed to extract bearer token from authorization header: %s', auth_header)
        raise LookupError('Invalid Bearer token')

    return bearer_token


def generate_api_gateway_response(status_code, headers=None, body=None):
    """Generate a lambda API Gateway response with a given status_code, headers dict, and
    jsonifyable body. The 'headers' and 'body' keys will not be present in the generated response
    if those fields are empty.
    """
    response = {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body)
    }

    return {k: v for k, v in response.items()
            if v and not v == 'null'}

def with_cors(allow_origin, allow_credentials, expose_headers=None):
    """Parametrized decorator that takes a function which returns an http response and returns
    a function that will add cors headers to the decorated functions http response.

    >>> @with_cors('website.com', True, 'Location')
    ... def func():
    ...     return { 'status_code': 201, 'headers': { 'Location': 'some uri' }}
    >>> func()
    {'status_code': 201, 'headers': {'Location': 'some uri', 'Access-Control-Allow-Origin': 'website.com', 'Access-Control-Allow-Credentials': True, 'Access-Control-Expose-Headers': 'Location'}}

    # Without headers
    >>> @with_cors('website.com', True)
    ... def func():
    ...     return {'status_code': 400}
    >>> func()
    {'status_code': 400, 'headers': {'Access-Control-Allow-Origin': 'website.com', 'Access-Control-Allow-Credentials': True, 'Access-Control-Expose-Headers': None}}

    >>>
    """
    def decorate(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            headers = response.get('headers', {})
            return {
                **response,
                'headers': {
                    **headers,
                    'Access-Control-Allow-Origin': allow_origin,
                    'Access-Control-Allow-Credentials': allow_credentials,
                    'Access-Control-Expose-Headers': expose_headers
                }
            }
        return inner
    return decorate
