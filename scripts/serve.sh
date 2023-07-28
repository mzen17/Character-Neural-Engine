#!/bin/bash
if [ "$1" == "dev" ] || [ "$1" == "test" ]; then
    export NODE_ENV=dev
    export LLAMA_SERVER="$2"
    poetry run uvicorn sxcne.main:app --reload --host 0.0.0.0 --port 4000

else
    export NODE_ENV=production
    export LLAMA_SERVER="10.42.0.227:8080"

    echo "Running in production mode!"
    poetry run uvicorn sxcne.main:app --host 0.0.0.0
fi
### This shell script is for running server on MacOS/Linux x86_64.