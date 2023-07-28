# Processor for LLM prompts depending on context.

def dialogueprocessor(message: str, familiarity: str, name: str, personality: str, context: str):
    return f"Transcript of a dialog, where {name} interacts with {familiarity}. {name} is {personality}. {context} {familiarity}: {message} | {name}:"

def emotionprocessor(message: str):
    return f"Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision. User: What emotions does someone saying this {message} have? Bob: The emotions, in order of most likely, are:"

def gencontextprocessor(backstory: str, name: str ):
    return f"Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision. User: What might {name} learn all these {backstory} happening? Any correlations he would see that he learns? (give the things he learns, short, in the format of 'Bob thinks (if extrapolated) or knows'. Bob:"