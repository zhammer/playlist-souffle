"""AWS lambda function for shuffling a playlist's tracks by artist or album."""

import logging
from urllib.parse import parse_qs
from spotipy import Spotify, SpotifyException
from souffle.exception import SouffleParameterError
from souffle.shuffle import souffle_playlist
from souffle.util import extract_bearer_token_from_api_event, generate_api_gateway_response

logger = logging.getLogger(__name__)

def generate_spotify_exception_response(exception):
    """Generate an api gateway response based on a spotify exception."""
    if exception.code == 401:
        return generate_api_gateway_response(401, message=exception.msg)
    else:
        return generate_api_gateway_response(
            500,
            message='Encountered error connecting to Spotify api. Message: "{}".'.format(exception.msg)
        )


def main(event, context):
    """AWS lambda event handler"""

    logger.debug('Handling event "%s". Context: "%s"', event, context)

    # Get access token
    try:
        access_token = extract_bearer_token_from_api_event(event)
    except LookupError as e:
        return generate_api_gateway_response(
            400,
            message=str(e)
        )

    # Extract request body
    request_body = parse_qs(event['body'])

    # Required fields
    try:
        playlist_uri = request_body['playlistUri'][0]
        shuffle_by = request_body['shuffleBy'][0]
        user_id = request_body['userId'][0]
    except KeyError as e:
        return generate_api_gateway_response(
            400,
            message='Missing field: "{}".'.format(e)
        )

    # Optional fields
    try:
        destination_uri = request_body['destinationUri'][0]
    except KeyError:
        destination_uri = None

    # Setup spotipy client
    try:
        spotify = Spotify(access_token)
    except SpotifyException as e:
        return generate_spotify_exception_response(e)


    # Souffle playlist
    try:
        souffle_playlist(playlist_uri, shuffle_by, user_id, spotify, destination_uri)
    except SouffleParameterError as e:
        return generate_api_gateway_response(400, message=e)
    except SpotifyException as e:
        return generate_spotify_exception_response(e)
    # except Exception as e:
    #     logger.error('Unexpected exception: "{}".'.format(e))
    #     return generate_api_gateway_response(500)

    # Return success
    return generate_api_gateway_response(200)
