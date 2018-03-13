#!/usr/bin/env bash
#
# Send a request to the /accesstoken endpoint to obtain a new access token from a valid refresh token.

REFRESH_TOKEN=$1

RESPONSE=$(curl -H "Authorization: Bearer ${REFRESH_TOKEN}" \
                https://wumxvuo5nb.execute-api.us-east-1.amazonaws.com/dev/accesstoken \
                -XPOST)

if [ ! "$RESPONSE" ]; then
    echo "Request failed"
    exit;
fi

echo "$RESPONSE" | python -m json.tool
