from fastapi import FastAPI
import json
import os
from sxcne.models.inputs import MessageRequest
import sxcne.processors.serverprocessor
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask/{character}/")
async def response(character: str, input: MessageRequest):
    print(character.lower())
    if (character.lower() == "minato" or character.lower() == "yuki" or character.lower() == "kento"):
        if(character.lower() == "minato"):
            spi = 1
        elif(character.lower() == "yuki"):
            spi=2
        else:
            spi=0
        print(spi)

        # Some weird code to get the path to the JSON file because I couldn't figure out how to do it otherwise
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, "characters.json")

        # Load JSON Data
        with open(json_file_path, "r") as file:
            json_data = file.read()
        characterdata = json.loads(json_data)

        # Get Character Data
        name = (characterdata["characters"][spi]["name"])
        personality = (characterdata["characters"][spi]["personality"])
        # backstory = (characterdata["characters"][0]["backstory"])

        # Paramaters
        message = input.message
        familiarity = "a stranger"

        # Get Response
        data = sxcne.processors.serverprocessor.post_message2server(message, familiarity, name, personality)
        return {"response": data["reply"], "emotions" : data["emotion"]}
    return {"error":"invalid character"}
