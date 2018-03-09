"""AWS lambda function for obtaining a spotify access token given a spotify refresh token."""

from base64 import b64decode
import logging
import os
import boto3
import requests

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
        params=payload
    )

    if response.status_code == requests.codes.ok:
        access_token = response.json()['access_token']
        logger.debug(
            'Successfully retrieved access token "***%s" for refresh token "***%s".',
            access_token[-4:],
            refresh_token[-4:]
        )
        return access_token

    # If the request fails, log the error and return None
    else:
        logger.info(
            'Failed to retrieve access token for refresh token "***%s". HTTP status: %s.',
            refresh_token[-4:],
            response.status_code
        )
        return None

# TODO: Move to common module
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


def main(event, context):
    """AWS lambda event handler"""

    logger.debug('Handling event "%s". Context: "%s"', event, context)

    # Get environment variables
    spotify_client_id = decrypt_kms_string(os.environ['SPOTIFY_CLIENT_ID'])
    spotify_client_secret = decrypt_kms_string(os.environ['SPOTIFY_CLIENT_SECRET'])

    # Get event variables
    refresh_token = event['refreshToken']

    # Fetch access token
    access_token = fetch_spotify_access_token(
        refresh_token,
        spotify_client_id,
        spotify_client_secret
    )

    # TODO: Research aws lambda standards of request/response return values.
    #
    # Return access token and (optional) error message
    # error_message = None if access_token else 'Failed to obtain access token'
    # payload = {
    #     'accessToken': access_token,
    #     'errorMessage': error_message
    # }
    # return payload

    # Return access token as a raw string
    return access_token
