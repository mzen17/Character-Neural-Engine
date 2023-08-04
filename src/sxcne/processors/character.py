import json
import os

def get_character_index(input: str, person_asking: str = None):
    character_mapping = {
        "minato": 0,
        "yuki": 1,
        "kento": 2,
    }

    # Input character
    print(type( input))
    character = input.lower()
    character_index = character_mapping.get(character, None)

    # Input person asking
    person_asking = person_asking.lower() if person_asking else None
    familiarity_mapping = {
        "minato": "a friend",
        "yuki": "a friend",
        "kento": "a friend",
    }

    # Determine familiarity
    familiarity = familiarity_mapping.get(person_asking, "a stranger")

    return character_index, familiarity

def get_character_data_from_index(index: int):

    # Get the JSON file using path joins
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "characters.json")

    # Load JSON Data
    with open(json_file_path, "r") as file:
        json_data = file.read()
    
    characterdata = json.loads(json_data)

    name = (characterdata["characters"][index]["name"])
    personality = (characterdata["characters"][index]["personality"])
    backstory = (characterdata["characters"][index]["backstory"])
    knowledge_base = characterdata["characters"][index]["learned"]

    return name, personality, backstory, knowledge_base