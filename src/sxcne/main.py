# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/SXPLv1.txt

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from sxcne.models.inputs import MessageRequest
import sxcne.processors.server as server

import sxcne.processors.database as db
import sxcne.processors.character as character
import sxcne.utilities as util


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

key=""

if "NODE_ENV" in os.environ and os.environ["NODE_ENV"] == "dev":
    prod_mode = False
else:
    prod_mode = True

openai_mode = False

if "BACKEND" in os.environ:
    if os.environ["BACKEND"] == "llama" and ("LLAMA_SERVER" in os.environ):
        server.set_server_url(os.environ["LLAMA_SERVER"])
        print(server.url)

    elif os.environ["BACKEND"] == "openai" and "KEY" in os.environ:
        if "AUTH_KEY" in os.environ:
            key = os.environ["AUTH_KEY"]
        else:
            print("CRITICAL ERROR: KEY WAS NOT SET!! APP WILL NOT WORK!")
            exit

        print("Deploying with OpenAI...")
        openai_mode = True
else:
    if(prod_mode):
        print("CRITICAL ERROR: BACKEND WAS NOT SET!! APP WILL NOT WORK!")
        exit
    else:
        print("Warning: Backend was not set. App will not work.")


@app.post("/ask/")
async def response(input: MessageRequest):
    if key != "" and input.key != "" and input.key != key:
        return {"error":"app requires key and you are missing private key"}

    # Ensure request validation
    print("SESSION: ", input.session)
    if (not prod_mode):
        print("Warning! This is a development session!")
    elif (input.session is None):
        raise HTTPException(status_code=403, detail="Your app must first grab a key from the /genkey/ endpoint. This is to validate sessions so user chats cannot step on top of each other.")
    elif (not db.authenticateSession(input.id, input.session)):
        raise HTTPException(status_code=401, detail="Your app session is out of date. Try to reload your browser")


    # Get Character Data using character processor
    index, familiarity = character.get_character_index(input.character, input.person_asking)
    name, personality, backstory, knowledge_base = character.get_character_data_from_index(index)

    # Paramaters
    message = input.message
    context = db.get_conversation(input.id)

    if (context == None):
        context = [[],'']

    response = server.post_message2server(message, familiarity, name, personality, context[0], backstory)
    emotion = server.get_emotions(message)

    db.push_conversation_to_chatID(input.id,input.message,response)
    return {"response": response, "emotions" : emotion}


# 25000 values to rotate from, max 25000 concurrent users
keys = list(range(1, 25000))
@app.get("/genkey/")
def generatekey():
    genkey = keys.pop(0)
    keys.append(genkey)
    db.purgeRowKey(genkey)
    token = db.spawnKey(genkey)
    
    return {"key":genkey, "token":token}

