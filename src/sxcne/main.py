from fastapi import FastAPI
import json
import os
from sxcne.models.inputs import MessageRequest
import sxcne.processors.serverprocessor

app = FastAPI()
@app.post("/ask/{character}/")
async def response(character: str, input: MessageRequest):
    # Some weird code to get the path to the JSON file because I couldn't figure out how to do it otherwise
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "characters.json")

    # Load JSON Data
    with open(json_file_path, "r") as file:
        json_data = file.read()
    characterdata = json.loads(json_data)

    # Get Character Data
    name = (characterdata["characters"][0]["name"])
    personality = (characterdata["characters"][0]["personality"])
    # backstory = (characterdata["characters"][0]["backstory"])

    # Paramaters
    message = input.message
    familiarity = "a stranger"

    # Get Response
    data = sxcne.processors.serverprocessor.post_message2server(message, familiarity, name, personality)
    return {"response": data["reply"], "emotions" : data["emotion"]}
