#!/bin/bash
response=$(curl "localhost:$3/genkey/")

key=$(echo "$response" | jq -r '.key')
session=$(echo "$response" | jq -r '.token')

echo $key " | " $session
datablock="{\"message\":\"$1\",\"id\": $key, \"session\":\"$session\", \"character\":\"$2\"}"
echo "$datablock"

time curl -X POST -H "Content-Type: application/json" -d "$datablock" "http://localhost:$3/ask/"

