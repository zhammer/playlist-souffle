#!/usr/bin/env bash
#
# Souffle a playlist by invoking the shuffle-playlist lambda function locally.

PLAYLIST_URI=$1
USER_ID=$2
SHUFFLE_BY=$3
ACCESS_TOKEN=$4

API_GATEWAY_JSON="
{
    \"headers\": {
        \"Authorization\": \"Bearer ${ACCESS_TOKEN}\"
    },
    \"body\": \"playlistUri=${PLAYLIST_URI}&shuffleBy=${SHUFFLE_BY}&userId=${USER_ID}\"
}
"

# Generate temp file with data
file=$(mktemp souffle-request.json.XXX)
echo $API_GATEWAY_JSON > $file

echo "== Request =="
echo $API_GATEWAY_JSON

echo
echo "== Sending to local shuffle-playlist lambda =="
sls invoke local -f shuffle-playlist -p $file --log


rm -fr $file
