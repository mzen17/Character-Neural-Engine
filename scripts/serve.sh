#!/bin/bash
if [ "$1" == "dev" ] || [ "$1" == "test" ]; then
    export NODE_ENV=dev
    export BACKEND="llama"
    export LLAMA_SERVER="$2"
    poetry run uvicorn sxcne.main:app --reload --host 0.0.0.0 --port 4000

elif [ "$1" == "llama" ]; then
    export NODE_ENV=production
    export BACKEND="llama"
    export LLAMA_SERVER="$2"

    echo "Using Llama as backend in production!"
    poetry run uvicorn sxcne.main:app --host 0.0.0.0

elif [ "$1" == "openai"]; then
    export NODE_ENV=production
    export BACKEND="openai"
    export KEY="$2"
    export ORG="$3"

    echo "Using OpenAI as backend in production!!"
    poetry run uvicorn sxcne.main:app --host 0.0.0.0

else 
    export NODE_ENV=production
    echo "Using variable backend. Make sure to manually set BACKEND, {KEY, ORG}, or LLAMA_SERVER!"
    poetry run uvicorn sxcne.main:app --host 0.0.0.0
fi

### This shell script is for running server on MacOS/Linux x86_64.