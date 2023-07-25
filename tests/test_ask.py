# FastAPI Libs
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Standard Testing Libs
import json

# Interal Imports
from sxcne.main import app

client = TestClient(app)

def test__status():
    data = {"id": "324", "message": "hi", "model": "orca-3b.q4_0.bin"}
    response = client.post("/ask/Minato/", data=json.dumps(data))
    assert response.status_code == 200

def test__response():
    data = {"id": "324", "message": "hi", "model": "orca-3b.q4_0.bin"}
    response = client.post("/ask/Minato/", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json() != {"message": "", "emotions": []}
