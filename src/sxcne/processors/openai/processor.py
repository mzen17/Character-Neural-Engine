import openai
import sxcne.processors.openai.prompt as promptprocessor
import sxcne.utilities as utils

def post_message2OpenAI(message:str, familiarity:str, name:str, personality:str, context:str, backstory: str):
        # Grab chat info and info
        context_merge = ""

        for chat in context:
            context_merge += f"{familiarity}: {chat['input']} "
            context_merge += f"{name}: {chat['output']}"

        # Get Response
        instruction, prompt = promptprocessor.openai_dialogueprocessor(message, familiarity, name, personality, context_merge, backstory)
        prompt = utils.get_last(prompt, 200)

        print(prompt)

        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=15,
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt}
            ])
        
        response = completion.choices[0].message.content
        response_data = utils.slash_sentences(utils.filter_out_text_between_asterisks(response))

        # Emotions
        emotions = get_emotions_openai(response)

        if (response_data == "" or response_data == " "):
            response_data = "..."

        return {"reply": response_data, "emotion": emotions}

def get_emotions_openai(message: str):
    prompt = message

    print("Emotions Prompt: ",prompt) # Logging purposes

    message = utils.get_last(message, 10)

    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=5,
            messages=[
                {"role": "user", "content": message}
        ])
    # emotion_data = utils.emotions_filter(completion.choices[0].message.content)
    emotion_data = completion.choices[0].message.content

    return emotion_data