#!/bin/bash
poetry run env $(cat .env | grep -v ^# | xargs) pytest -k "$1"