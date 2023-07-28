# FastAPI Libs
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Standard Testing Libs
import os

# Interal Imports
from sxcne.main import app

client = TestClient(app)

def test__status():
    os.environ["NODE_ENV"] = "prod"
    os.environ["LLAMA_SERVER"] = "10.42.0.227:8080"

    response = client.get("/genkey/").json()

    key = response["key"]
    session = response["token"]
    print("Data: ",key, session)
    
    data = {"id": key, "message": "hi", "character": "minato", "session": session}
    response = client.post("/ask/", json=data)
    assert response.status_code == 200
    assert response.json() != {"message": "", "emotions": []}
