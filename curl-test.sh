#!/usr/bin/env bash

set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"
ENDPOINT="${BASE_URL}/api/timeline_post"

# Create unique test data so each run creates a different post.
RANDOM_ID="$(date +%s)-${RANDOM}"

NAME="Curl Test ${RANDOM_ID}"
EMAIL="curl-test-${RANDOM_ID}@example.com"
CONTENT="Automated timeline test ${RANDOM_ID}"

echo "Testing timeline API at:"
echo "$ENDPOINT"
echo

echo "1. Creating a random timeline post..."

POST_RESPONSE=$(curl \
  --silent \
  --show-error \
  --fail \
  --request POST \
  "$ENDPOINT" \
  --data-urlencode "name=$NAME" \
  --data-urlencode "email=$EMAIL" \
  --data-urlencode "content=$CONTENT")

echo "POST response:"
echo "$POST_RESPONSE"
echo

echo "2. Retrieving all timeline posts..."

GET_RESPONSE=$(curl \
  --silent \
  --show-error \
  --fail \
  "$ENDPOINT")

echo "GET response:"
echo "$GET_RESPONSE"
echo

echo "3. Checking whether the new post was added..."

if printf '%s' "$GET_RESPONSE" | grep -Fq "$CONTENT"; then
  echo "SUCCESS: The timeline post was created and found."
else
  echo "FAILURE: The timeline post was not found."
  exit 1
fi