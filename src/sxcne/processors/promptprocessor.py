# Processor for LLM prompts depending on context.

def dialogueprocessor(message: str, familiarity: str, name: str, personality: str, context: str):
    return f"Transcript of a dialog, where {name} interacts with {familiarity}. {name} is {personality}. {context} {familiarity}: {message} | {name}:"

def emotionprocessor(message: str, familiarity: str, name: str, personality: str):
    return f"Question and Answer session. Question: What emotions does someone saying this {message} have? Answer: The emotions, in order of most likely, are:"
