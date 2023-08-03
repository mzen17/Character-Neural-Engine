#!/bin/bash

# For usage outside of the docker container to start it
source .env

docker stop sxcne -t 5
docker rm sxcne

docker run -p 8000:8000 --name sxcne -e BACKEND=$BACKEND -e LLAMA_SERVER=$LLAMA_SERVER -e ORG=$ORG -e KEY=$KEY -it sxcne
