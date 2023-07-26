#!/bin/bash
time curl -X POST  -H "Content-Type: application/json" -d '{"message":"'"$1"'","id": "304"}' http://192.168.4.25:8000/ask/"$2"/

