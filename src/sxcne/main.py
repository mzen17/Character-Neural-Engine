from fastapi import FastAPI
from sxcne.models.inputs import MessageRequest

app = FastAPI()

@app.post("/ask/{character}/")
async def response(character: str, input: MessageRequest):
    
    if (character in ["Minato", "Yuki", "Kento"]):
        validchar  = True
    else:
        validchar = False

    if not validchar:
        return {"message": "invalid_character"}

    # Fetch response to server to update. Currently in testing, so will use random
    responses = ["happy", "sad", "angry", "neutral"]
    message = "I'm happy!"

    return {"message": message, "emotions": responses}

