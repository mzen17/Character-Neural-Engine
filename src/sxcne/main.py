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
@app.get("/test")
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

    # GPT4ALL Snoozy 13B
    model = GPT4All("GPT4All-13B-snoozy.ggmlv3.q4_0.bin")

    # Paramaters
    message = "Hey, you want an apple?"
    extras = "Include only the response, not anything else such as 'example', 'she might say', etc."
    familiarity = "stranger"

    # Get Response
    format_string = f"Write a single response in her personaltiy to a {familiarity} asking her {message}. If there is not enough information, extrapolate something up. {extras}"
    prompt = f"{name} is {personality}. {format_string}"
    output = model.generate(prompt, max_tokens=50, temp=1.5)

    # Get Emotions
    format_string = f"Write the emotion that {name} would feel to a {familiarity} asking her {message}. Append a emotion even if it not enough details. Guess."
    prompt = f"{name} is {personality}. {format_string}"

    emotions = model.generate(prompt, max_tokens=50, temp=0.5)

    return {"output": output, "emotions": emotions}