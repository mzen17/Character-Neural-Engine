# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/sxpl.txt

import requests
from typing import List

# Internal Libs
import sxcne.processors.promptprocessor as promptprocessor
import sxcne.utilities as utils

url = ""


def set_server_url(url_input: str):
    global url
    url = "http://" + url_input
    print("URL: ", url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for unsuccessful responses (4xx or 5xx)
        print("Backend URL connection successful. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Warning, Llama server connection failed:", e)


def post_message2server(message:str, familiarity:str, name:str, personality:str, context:str, backstory: str):
    # Grab chat info and info
    context_merge = ""

    for chat in context:
        context_merge += f"{familiarity}: {chat['input']} "
        context_merge += f"{name}: {chat['output']}"

    # Get Response
    prompt = promptprocessor.dialogueprocessor(message, familiarity, name, personality, context_merge, backstory)
    print("Prompt: ",prompt)

    data = {"prompt": prompt,"n_predict": 64, "temperature":0.5}
    response = requests.post(url+"/completion", json = data).json()
    response_data = utils.slash_sentences(utils.filter_out_text_between_asterisks(response["content"]))

    # Emotions
    emotions = get_emotions(message)

    if (response_data == "" or response_data == " "):
        response_data = "..."

    return {"reply": response_data, "emotion": emotions}


def create_context_from_backstory(backstory: str, name: str):
    event_merge = ""

    for event in backstory:
        event_merge = event_merge + event + ", "

    prompt = promptprocessor.gencontextprocessor(event_merge, name)
    data = {"prompt": prompt,"n_predict": 128, "temperature":0.1}
    response = requests.post(url+"/completion", json = data).json()
    response_data = utils.slash_sentences(response["content"])

    print(prompt)

    return response_data
    
def get_emotions(message: str):
    prompt = promptprocessor.emotionprocessor(message)
    data = {"prompt": prompt,"n_predict": 16, "temperature":0.1}

    print("Emotions Prompt: ",prompt) # Logging purposes

    emotion = requests.post(url+"/completion", json = data).json()
    print (emotion["content"])
    emotion_data = utils.emotions_filter(emotion["content"])

    return emotion_data

    

    