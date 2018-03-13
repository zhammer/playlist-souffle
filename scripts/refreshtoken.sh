#!/usr/bin/env bash
#
# Send a request to the /refreshtoken endpoint to obtain a refresh token and access token from
# a spotify authorization code. To obtain the authorization code, visit the following link in a
# browser, and extract the 'code=' url param.
#
# https://accounts.spotify.com/authorize?client_id=b231329aba1a4c539375436a267db917&response_type=code&redirect_uri=https://127.0.0.1:8100&scope=playlist-modify-public
#
# Note: client id is not a secret. Redirect uri must be https://127.0.0.1:8100 as it's whitelisted.
#       can change the scope on the request to include playlist-modify-private for private playlists.

AUTH_CODE=$1

RESPONSE=$(curl -H "Authorization: Bearer ${AUTH_CODE}" \
                -d redirectUri=https%3A%2F%2F127.0.0.1%3A8100 \
                https://wumxvuo5nb.execute-api.us-east-1.amazonaws.com/dev/refreshtoken)

if [ ! "$RESPONSE" ]; then
    echo "Request failed"
    exit;
fi

echo "$RESPONSE" | python -m json.tool
