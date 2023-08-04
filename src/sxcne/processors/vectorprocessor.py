# Processor for generating embeddings for efficient cache

import torch
from transformers import AutoTokenizer, AutoModel

# Load the Sentence-BERT model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def generate_sentence_embedding(sentence):

    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        output = model(**inputs)

    sentence_embedding = output.last_hidden_state[:, 0, :]
    normalized_embedding = torch.nn.functional.normalize(sentence_embedding)
    sentence_vector = normalized_embedding.squeeze().tolist()
    
    return sentence_vector
