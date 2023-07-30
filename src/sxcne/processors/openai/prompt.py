def openai_dialogueprocessor(message: str, familiarity: str, name: str, personality: str, context: str, knowledgebase: str):
    return f"A chat between {name}, and {familiarity}. {name} is {personality}, and knows {knowledgebase}. {context}", f"{message}. {name}:"
