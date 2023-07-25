# Class for handling connections to server.
import requests
import sxcne.processors.promptprocessor
import sxcne.utilities

def post_message2server(message:str, familiarity:str, name:str, personality:str):
    url = 'http://localhost:8080/completion'

    # Get Response
    prompt = sxcne.processors.promptprocessor.dialogueprocessor(message, familiarity, name, personality)
    data = {"prompt": prompt,"n_predict": 64, "temperature":0.3}

    print(prompt) # Logging purposes

    response = requests.post(url, json = data).json()
    print (response["content"])
    response_data = sxcne.utilities.filter_out_text_between_asterisks(response["content"])
    response_data = sxcne.utilities.slash_sentences(response_data)

    # Emotions
    prompt = sxcne.processors.promptprocessor.emotionprocessor(message, familiarity, name, personality)
    data = {"prompt": prompt,"n_predict": 16, "temperature":0.1}

    print(prompt) # Logging purposes

    emotion = requests.post(url, json = data)
    emotion_data = emotion.json()

    return {"reply": response_data, "emotion": emotion_data["content"]}