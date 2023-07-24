from fastapi import FastAPI
from gpt4all import GPT4All
import json
import os
from sxcne.models.inputs import MessageRequest

app = FastAPI()

# Production Code
@app.post("/ask/{character}/")
async def response(character: str, input: MessageRequest):
    
    if (character in ["Minato", "Yuki", "Kento"]):
        validchar  = True
    else:
        validchar = False

    if not validchar:
        return {"message": "invalid_character"}

    # Fetch response to server to update. Currently in testing, so will use random
    responses = ["happy", "sad", "angry", "neutral"]
    message = "I'm happy!"

    model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")
    output = model.generate("The capital of France is ", max_tokens=3)
    print(output)

    return {"output": output}

format_string = ""


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
    model = GPT4All("guanaco-33B.ggmlv3.q4_0.bin", model_path="models/", n_threads=12)

    # Paramaters
    message = "How are you doing today?"
    extras = "only the response, not anything else such as 'example', 'she might say', your comments, etc"
    familiarity = "a stranger"

    # Get Response
    format_string = f"Write {name}'s detailed reply with the format of {extras} in her personaltiy of {personality}, to {familiarity} asking her the following: {message}."
    prompt = f"{format_string}"
    output = model.generate(prompt, max_tokens=150, temp=2)

    # Get Emotions
    format_string = f"Find the emotion {name} would feel if a {familiarity} asked her {message}. Append a emotion even if it not enough details."
    extras = "Use only a single word for your answer, not anything else such as 'If I were her', 'her emotions probably are'"
    prompt = f"{name} is {personality}. {format_string}, {extras}."

    emotions = model.generate(prompt, max_tokens=10, temp=0.1)

    return {"output": output}