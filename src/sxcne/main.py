# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/sxpl.txt

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import json
import os

from sxcne.models.inputs import MessageRequest
import sxcne.processors.serverprocessor as server
import sxcne.processors.databaseprocessor as db


app = FastAPI()
db.cleanup()
db.initialize()

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

server.set_server_url(os.environ["LLAMA_SERVER"])
print(server.url)

@app.post("/ask/")
async def response(input: MessageRequest):
    server.set_server_url(os.environ["LLAMA_SERVER"])

    # Ensure request validation
    print("SESSION: ", input.session)
    if (os.environ['NODE_ENV'] == "dev"):
        print("Warning! This is a development session!")
    elif (input.session is None):
        raise HTTPException(status_code=418, detail="Your app must first grab a key from the /genkey/ endpoint. This is to validate sessions so user chats cannot step on top of each other.")
    elif (not db.authenticateSession(input.id, input.session)):
        raise HTTPException(status_code=401, detail="Your app session is out of date. Try to reload your browser")

    # Some mapping checks. May be simplified in the future
    if(input.character.lower() == "minato"):
        spi = 0
    elif(input.character.lower() == "yuki"):
        spi=1
    elif(input.character.lower() == "kento"):
        spi=2
    else:
        return {"error":"invalid character"}


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
    backstory = (characterdata["characters"][0]["backstory"])

    for event in backstory:
        pass

    # Paramaters
    message = input.message
    familiarity = "a stranger"

    context = db.get_conversation(input.id)

    if (context == None):
        context = [[],'']

    # Get Response
    data = server.post_message2server(message, familiarity, name, personality, context[0])
    db.push_conversation_to_chatID(input.id,input.message,data["reply"])

    return {"response": data["reply"], "emotions" : data["emotion"]}

keys = list(range(1, 25000))

@app.get("/genkey/")
def generatekey():
    genkey = keys.pop(0)
    keys.append(genkey)
    db.purgeRowKey(genkey)
    token = db.spawnKey(genkey)
    
    return {"key":genkey, "token":token}
    

