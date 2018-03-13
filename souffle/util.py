"""Module for util functions in the playlist souffle service.

Available functions:
- decrypt_kms_string: Decrypt a kms-encrypted string.
- extract_bearer_token: Extract a bearer token from a Bearer auth header.
- extract_bearer_token_from_api_event: Extract a bearer token from an API Gateway event.
- generate_api_gateway_response: Generate an api gateway response with a statuscode and json body.
"""

from base64 import b64decode
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
    """Generate an http response for a lambda API Gateway proxy function with a given status
    code, headers and body.

    Args:
        status_code: Integer of http status code
        headers: Dictionary of response headers
        body: Response body (will be converted to json).

    Returns:
        Dict representation of response

    >>> generate_api_gateway_response(200, body={'message':'Success!'})
    {'statusCode': 200, 'body': '{"message": "Success!"}'}

    """
    response = {
        'statusCode': status_code
    }
    if headers:
        response['headers'] = headers
    if body:
        response['body'] = json.dumps(body)

    return response
