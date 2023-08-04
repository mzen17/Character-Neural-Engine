# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/sxpl.txt

import requests
import openai
import os

# Internal Libs
import sxcne.processors.prompt as promptprocessor
import sxcne.processors.cache as cache
import sxcne.utilities as utils


url = ""
openai.api_key = os.getenv("KEY")
openai.organization = os.getenv("ORG")



def set_server_url(url_input: str):
    global url
    url = "http://" + url_input
    print("URL: ", url)
    
    # Test URL to see if it works.
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

    # Check cache and return instantly if cache is found
    cached_response = cache.getCached(context_merge +" " + name + " " + message)
    if cached_response != None:
        return cached_response
    

    # Get Response
    if ("BACKEND" in os.environ and os.environ["BACKEND"] == "openai"):
        instruction, prompt = promptprocessor.openai_dialogueprocessor(message, familiarity, name, personality, context_merge, backstory)
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=15,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": prompt}
        ])
        response = completion.choices[0].message.content
    
    else:

        prompt = promptprocessor.dialogueprocessor(message, familiarity, name, personality, context_merge, backstory)
        print("Prompt: ",prompt)
        data = {"prompt": prompt,"n_predict": 30, "temperature":0.5}
        response = requests.post(url+"/completion", json = data).json()

    response_data = utils.slash_sentences(utils.filter_out_text_between_asterisks(response["content"]))

    if (response_data == "" or response_data == " "):
        response_data = "..."

    # Cache response
    cache.updateCache(context_merge +" " + name + " " + message, response_data)
    return response_data


def create_context_from_backstory(backstory: str, name: str):
    event_merge = ""

    for event in backstory:
        event_merge = event_merge + event + ", "

    prompt = prompt.gencontextprocessor(event_merge, name)

    # Params
    data = {"prompt": prompt,"n_predict": 128, "temperature":0.1}
    response = requests.post(url+"/completion", json = data).json()
    response_data = utils.slash_sentences(response["content"])

    print(prompt) # Log prompt

    return response_data

def create_context_from_backstory(backstory: str, name: str):
    event_merge = ""

    for event in backstory:
        event_merge = event_merge + event + ", "

    prompt = prompt.gencontextprocessor(event_merge, name)
    data = {"prompt": prompt,"n_predict": 128, "temperature":0.1}
    response = requests.post(url+"/completion", json = data).json()
    response_data = utils.slash_sentences(response["content"])

    print(prompt) # Log prompt

    return response_data
    

def get_emotions(message: str):
    return cache.get_emotion(message)

