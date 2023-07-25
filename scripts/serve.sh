#!/bin/bash

if [ "$1" == "prod" ]; then
    poetry run uvicorn sxcne.main:app --host 0.0.0.0
else
    poetry run uvicorn sxcne.main:app --reload
fi



### This shell script is for running server on MacOS/Linux x86_64.