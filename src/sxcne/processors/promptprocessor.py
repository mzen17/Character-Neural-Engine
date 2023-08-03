# Processor for LLM prompts depending on context.

def dialogueprocessor(message: str, familiarity: str, name: str, personality: str, context: str, knowledgebase: str):
    return f"Transcript of a dialog, where {name} interacts with {familiarity}. {name} is {personality}, and has experienced {knowledgebase}. {context} {familiarity}: {message}. {name}:"

def emotionprocessor(message: str):
    return f"Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision. User: What emotions does someone saying this {message} have? Bob: The emotions, in order of most likely, are:"

def gencontextprocessor(backstory: str, name: str ):
    return f"Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision in the format of list, with '{name} thinks (if extrapolated) or knows'. User: What correlations might {name} extrapolate from the events(  {backstory}, ) happening?. Bob: {name} extrapolates that"