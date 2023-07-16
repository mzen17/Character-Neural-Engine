from fastapi import FastAPI
import json
from fastapi.testclient import TestClient
from sxcne.main import app

client = TestClient(app)

def test__status():
    data = {"id": "324", "message": "hi"}
    response = client.post("/ask/Minato/", data=json.dumps(data))
    assert response.status_code == 200

def test__response():
    data = {"id": "324", "message": "hi"}
    response = client.post("/ask/Minato/", data=json.dumps(data))
    assert response.status_code == 200
    assert response.json() == {"message": "I'm happy!", "emotions": ["happy", "sad", "angry", "neutral"]}
