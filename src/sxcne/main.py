# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/SXPLv1.txt

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai

import json
import os

from sxcne.models.inputs import MessageRequest
import sxcne.processors.serverprocessor as server
import sxcne.processors.openai.processor as openai_server
import sxcne.processors.databaseprocessor as db


app = FastAPI()
db.cleanup()
db.initialize()
openai.api_key = os.getenv("KEY")
openai.organization = os.getenv("ORG")


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
        return {"error":"app rqeuires key and you are missing private key"}

    # Ensure request validation
    print("SESSION: ", input.session)
    if (not prod_mode):
        print("Warning! This is a development session!")
    elif (input.session is None):
        raise HTTPException(status_code=418, detail="Your app must first grab a key from the /genkey/ endpoint. This is to validate sessions so user chats cannot step on top of each other.")
    elif (not db.authenticateSession(input.id, input.session)):
        raise HTTPException(status_code=401, detail="Your app session is out of date. Try to reload your browser")

    # Some mapping checks. May be simplified in the future
    chararacter = input.character.lower()
    if(chararacter == "minato"):
        character_index = 0
    elif(chararacter == "yuki"):
        character_index=1
    elif(chararacter == "kento"):
        character_index=2
    else:
        return {"error":"invalid character"}
    
    if (input.person_asking is not None):
        if(input.person_asking.lower() == "minato"):
            familiarity = "a friend"
        elif(input.person_asking.lower() == "yuki"):
            familiarity = "a friend"
        elif(input.person_asking.lower() == "kento"):
            familiarity = "a friend"
        else:
            familiarity = "a stranger"
    else:
        familiarity = "a stranger"
    


    # Some weird code to get the path to the JSON file because I couldn't figure out how to do it otherwise
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "characters.json")

    # Load JSON Data
    with open(json_file_path, "r") as file:
        json_data = file.read()
    
    characterdata = json.loads(json_data)

    # Get Character Data
    name = (characterdata["characters"][character_index]["name"])
    personality = (characterdata["characters"][character_index]["personality"])
    backstory = (characterdata["characters"][character_index]["backstory"])

    if not openai_mode:
        # knowledge_base = server.create_context_from_backstory(backstory, name)
        knowledge_base = characterdata["characters"][character_index]["learned"]
        print(knowledge_base)
    else:
        knowledge_base = characterdata["characters"][character_index]["learned"]

    # Paramaters
    message = input.message
    context = db.get_conversation(input.id)

    if (context == None):
        context = [[],'']

    # Check Cache
    if (db.check_cache(message + " " + str(familiarity) + " " +  name + " " + str(context[0]))):
        response = db.get_cache(message + " " + str(familiarity) + " " +  name + " " + str(context[0]))
        print("Using cache to serve response.")
    else:
        # Get Response
        if openai_mode:
            response = openai_server.post_message2OpenAI(message, familiarity, name, personality, context[0], backstory)
        else:
            response = server.post_message2server(message, familiarity, name, personality, context[0], backstory)
        db.set_cache(message + " " + str(familiarity) + " " +  name + " " + str(context[0]), response)

    if (db.check_cache(message)):
        emotion = db.get_cache(message)
    else:
        emotion = server.get_emotions(message)
        db.set_cache(message, emotion)

    db.push_conversation_to_chatID(input.id,input.message,response)
    return {"response": response, "emotions" : emotion}

keys = list(range(1, 25000))

@app.get("/genkey/")
def generatekey():
    genkey = keys.pop(0)
    keys.append(genkey)
    db.purgeRowKey(genkey)
    token = db.spawnKey(genkey)
    
    return {"key":genkey, "token":token}

