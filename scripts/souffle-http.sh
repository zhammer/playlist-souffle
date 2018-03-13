#!/usr/bin/env bash
#
# Souffle a playlist by invoking the shuffle-playlist lambda via the /souffle endpoint.

PLAYLIST_URI=$1
USER_ID=$2
SHUFFLE_BY=$3
ACCESS_TOKEN=$4

ENDPOINT_URL='https://wumxvuo5nb.execute-api.us-east-1.amazonaws.com/dev/souffle'

RESPONSE=$(curl -H "Authorization: Bearer ${ACCESS_TOKEN}" \
                -d playlistUri="$PLAYLIST_URI" \
                -d userId="$USER_ID" \
                -d shuffleBy="$SHUFFLE_BY" \
                $ENDPOINT_URL \
                -i)

if [ ! "$RESPONSE" ]; then
    echo "Request failed"
    exit;
fi

echo "$RESPONSE"
