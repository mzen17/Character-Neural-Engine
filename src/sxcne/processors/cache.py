from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import sxcne.processors.database as db


def getCached(input: str):
    return db.get_cache(getEmbeddings(input), 0.4)


def updateCache(input: str, output: str):
    vector = getEmbeddings(input)
    db.set_cache(vector, output)


def getEmbeddings(input: str):
    model = SentenceTransformer('thenlper/gte-small')
    return model.encode(input).tolist()


def get_emotion(text):
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
    model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")

    input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

    output = model.generate(input_ids=input_ids,
        max_length=2)

    dec = [tokenizer.decode(ids) for ids in output]
    label = dec[0]
    return label