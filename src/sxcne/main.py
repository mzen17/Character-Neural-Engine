from fastapi import FastAPI
from gpt4all import GPT4All
import json
import os
from sxcne.models.inputs import MessageRequest

app = FastAPI()

format_string = ""
modelbin = "ggml-llama2-13B-model-q4_0.bin"
modelpath = "models/"

# Production Code
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
    backstory = (characterdata["characters"][0]["backstory"])

    # GPT4ALL Guanaco Model. Note: Needs to be swapped in prod as this is a noncommercial model.
    print(os.cpu_count()/2)
    model = GPT4All(modelbin, model_path=modelpath, n_threads=(int(os.cpu_count()/2)))

    # Paramaters
    message = MessageRequest.message
    familiarity = "a friend"

    # Get Response
    extras = "only the reply, not anything else such as 'example', 'she might say', your comments, etc"
    format_string = f"Write {name}'s reply with her personaltiy of {personality}, to {familiarity} asking her the following: {message}."
    prompt = f"{format_string}"

    response = model.generate(prompt, max_tokens=50, temp=0.1)

    # Get Emotions
    format_string = f"Predict {name}'s emotion, her personality of {personality} if a {familiarity} asked her the following: {message}."
    extras = "Use only a single word for your answer, not anything else such as 'If I were her', 'her emotions probably are'"
    prompt = f"{format_string}, {extras}."

    emotions = model.generate(prompt, max_tokens=10, temp=0.1)

    return {"response": response, "emotions" : emotions}

# Testing Code. DO NOT USE IN PRODUCTION!!!
@app.get("/test/")
async def testing():
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
    backstory = (characterdata["characters"][0]["backstory"])

    # GPT4ALL Guanaco Model. Note: Needs to be swapped in prod as this is a noncommercial model.
    print(os.cpu_count()/2)
    model = GPT4All(modelbin, model_path=modelpath, n_threads=(int(os.cpu_count()/2)))

    # Paramaters
    message = "How are you doing today?"
    familiarity = "a friend"

    # Get Response
    extras = "only the reply, not anything else such as 'example', 'she might say', your comments, etc"
    format_string = f"Write {name}'s reply with her personaltiy of {personality}, to {familiarity} asking her the following: {message}."
    prompt = f"{format_string}"

    response = model.generate(prompt, max_tokens=50, temp=0.1)

    # Get Emotions
    format_string = f"Predict {name}'s emotion, her personality of {personality} if a {familiarity} asked her the following: {message}."
    extras = "Use only a single word for your answer, not anything else such as 'If I were her', 'her emotions probably are'"
    prompt = f"{format_string}, {extras}."

    emotions = model.generate(prompt, max_tokens=10, temp=0.1)

    return {"response": response, "emotions" : emotions}

@app.get("/env_test/")
async def env_test():
    environment = "forest"
    quest = "Find the route to the cube."
    map = [[2,0,0],[0,0,1],[0,0,0]]
    dictionary = "0 is a space, 1 is the player, 2 is a cube."
    format = "Return your answer as a list of directions, such as 'up', 'right', 'down', 'left'"
    prompt = f"Instruction: {format}. Prompt: You are in a {environment}. The map is {map}. {quest}. {dictionary}"

    model = GPT4All(modelbin, model_path=modelpath, n_threads=8)
    instruction = model.generate(prompt, max_tokens=50, temp=0.1)

    print(instruction)

    return instruction