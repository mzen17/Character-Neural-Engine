# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/SXPLv1.txt

# Utilities class for processing output of LLMs

import re

def filter_out_text_between_asterisks(text: str):
    return re.sub('\(.*?\)', '',re.sub('\*.*?\*', '', text))

# Sentence slasher that removes all text from the last punctation before a colon to the end of the string. Useful to ensure that there is no trailing text.
def slash_sentences(sentence):
    last = 0
    for i in range(len(sentence)):
        if sentence[i] == "." or sentence[i] == "?" or sentence[i] == "!":
            last = i
        if sentence[i] == ":":
            sentence = sentence[:last+1]
            break
    return sentence

# Return a list of emotions that appear from a string
def emotions_filter(sentence: str):
    common_emotions = [
    "Happy", "Sad", "Angry", "Excited", "Fearful", "Calm", "Surprised",
    "Anxious", "Content", "Confident", "Disgusted", "Grateful", "Hopeful",
    "Jealous", "Lonely", "Nervous", "Peaceful", "Proud", "Relaxed", "Shocked",
    "Stressed", "Tired", "Bored", "Curious", "Frustrated", "Guilty",
    "Indifferent", "Joyful", "Regretful", "Satisfied", "Silly", "Unsure",
    "Worried", "Enthusiastic", "Insecure", "Loving", "Optimistic",
    "Embarrassed", "Hurt", "Amused", "Pensive", "Disappointed", "Ashamed",
    "Motivated", "Apprehensive", "Rejected", "Relieved", "Hopeless",
    "Gloomy", "Restless", "Inspired", "Giddy", "Determined", "Grumpy",
    "Impatient", "Ecstatic", "Suspicious", "Devastated", "Startled",
    "Satisfied", "Surprised", "Irritated", "Overwhelmed", "Panicked",
    "Appreciated", "Contempt", "Rejuvenated", "Sentimental", "Sneaky",
    "Fulfilled", "Enraged", "Guilty", "Pity", "Displeased", "Amused",
    "Vulnerable", "Resentful", "Fulfilled", "Overjoyed", "Ignored",
    "Isolated", "Worthless", "Insignificant", "Defiant", "Ambivalent",
    "Disrespected", "Inspired", "Cautious", "Powerless", "Disconnected",
    "Suspenseful", "Restless", "Yearning", "Disenchanted", "Embodied",
    "Lethargic", "Hesitant", "Detached", "Unloved", "Exhausted", "Anticipating",
    "Defeated", "Hostile", "Caring", "Restful", "Longing", "Content",
    "Alarmed", "Cautious", "Discontented", "Flustered", "Dismayed",
    "Fulfilled", "Eager", "Proud", "Determined", "Impulsive", "Touched",
    "Envious", "Indecisive", "Rejected", "Alive", "Fearless", "Helpless",
    "Astonished", "Lost", "Self-conscious", "Wistful", "Energetic",
    "Spiteful", "Enraged", "Pessimistic", "Tense", "Defensive", "Depressed",
    "Hurt", "Empowered", "Dismissive", "Resigned", "Dismissive", "Apathetic",
    "Horrified", "Disappointed", "Fascinated", "Fulfilled", "Fulfilled",
    "Reflective", "Despressed", "Mad", "Annoyed", "Confused", "Disappointed",
    "Excitement", "Happiness"
    ]

    # Convert the sentence to lowercase for case-insensitive matching
    sentence_lower = sentence.lower()
    result = []

    # Iterate through the emotions in the dictionary
    for emotion in common_emotions:
        # Convert the emotion to lowercase for case-insensitive matching
        emotion_lower = emotion.lower()

        # Check if the emotion exists in the sentence
        if emotion_lower in sentence_lower:
            result.append(emotion)

    return result

def get_last(input_string, amount):
    return input_string[-amount:]

from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")

model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")

def get_emotion(text):
  input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

  output = model.generate(input_ids=input_ids,
               max_length=2)
  
  dec = [tokenizer.decode(ids) for ids in output]
  label = dec[0]
  return label

