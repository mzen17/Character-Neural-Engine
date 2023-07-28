#!/bin/bash
echo $4
if [ "$4" == "m" ]; then
    key="$5"
    session="$6"
    echo "Using existing keys and sesions:" $5 "|" $6
else
    response=$(curl "localhost:$3/genkey/")
    key=$(echo "$response" | jq -r '.key')
    session=$(echo "$response" | jq -r '.token')
    echo $key " | " $session
fi

datablock="{\"message\":\"$1\",\"id\": $key, \"session\":\"$session\", \"character\":\"$2\"}"
echo "$datablock"

time curl -X POST -H "Content-Type: application/json" -d "$datablock" "http://localhost:$3/ask/"

