# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/sxpl.txt

import requests
import sxcne.processors.promptprocessor
import sxcne.utilities

def post_message2server(message:str, familiarity:str, name:str, personality:str, context:str):
    url = 'http://10.42.0.227:8080/completion'

    context_merge = ""

    for chat in context:
        context_merge += f"{familiarity}: {chat['input']} "
        context_merge += f"{name}: {chat['output']}"

    # Get Response
    prompt = sxcne.processors.promptprocessor.dialogueprocessor(message, familiarity, name, personality, context_merge)
    data = {"prompt": prompt,"n_predict": 64, "temperature":1}

    print(prompt) # Logging purposes

    response = requests.post(url, json = data).json()
    print (response["content"])
    response_data = sxcne.utilities.slash_sentences(sxcne.utilities.filter_out_text_between_asterisks(response["content"]))

    # Emotions
    prompt = sxcne.processors.promptprocessor.emotionprocessor(message, familiarity, name, personality)
    data = {"prompt": prompt,"n_predict": 16, "temperature":0.1}

    print(prompt) # Logging purposes

    emotion = requests.post(url, json = data).json()
    print (emotion["content"])
    emotion_data = sxcne.utilities.emotions_filter(emotion["content"])

    return {"reply": response_data, "emotion": emotion_data}
