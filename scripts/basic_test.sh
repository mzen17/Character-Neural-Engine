#!/bin/bash
time curl -X POST  -H "Content-Type: application/json" -d '{"message":"'$1'","id": '$3', "session":"'$4'", "character":"'$2'"}' http://localhost:4000/ask/"$2"/

