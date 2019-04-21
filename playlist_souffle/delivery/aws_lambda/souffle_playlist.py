"""AWS lambda function for shuffling a playlist's tracks by artist or album."""
import json
import logging
import os
from datetime import datetime as dt

from playlist_souffle import souffle_playlist
from playlist_souffle.definitions.exception import (SouffleParameterError,
                                                    SouffleSpotifyError)
from playlist_souffle.delivery.aws_lambda.util import (extract_bearer_token_from_api_event,
                                                       generate_api_gateway_response,
                                                       setup_sentry,
                                                       with_cors)
from playlist_souffle.gateways.spotify import SpotifyGateway

logger = logging.getLogger(__name__)

if os.environ.get('AWS_EXECUTION_ENV'):
  setup_sentry()

def generate_spotify_exception_response(exception):
    """Generate an api gateway response based on a spotify exception."""
    if exception.http_status == 401:
        return generate_api_gateway_response(401, body={'message': exception.message})
    else:
        return generate_api_gateway_response(
            500,
            body={
                'message': 'Encountered Spotify api error. Message: "{}".'.format(exception.message)
            }
        )

@with_cors('https://playlistsouffle.com', True, 'Location')
def handler(event, context):
    """AWS lambda event handler"""
    logger.debug('Handling event "%s". Context: "%s"', event, context)

    try:
        access_token = extract_bearer_token_from_api_event(event)
    except LookupError as e:
        return generate_api_gateway_response(400, body={'message': 'Missing or invalid authorization'})

    body = json.loads(event['body'])
    try:
        playlist_uri = body['playlistUri']
        souffle_by = body['souffleBy']
    except LookupError as e:
        return generate_api_gateway_response(400, body={'message': 'Missing field: "{}".'.format(e)})

    try:
        spotify = SpotifyGateway(access_token)
    except SouffleSpotifyError as e:
        return generate_spotify_exception_response(e)

    try:
        souffled_playlist_uri = souffle_playlist(spotify, playlist_uri, souffle_by, dt.now())
    except SouffleParameterError as e:
        return generate_api_gateway_response(400, body={'message': e})
    except SouffleSpotifyError as e:
        return generate_spotify_exception_response(e)

    return generate_api_gateway_response(201, headers={'Location': souffled_playlist_uri})
