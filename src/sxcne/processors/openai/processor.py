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


        return response_data

def get_emotions_openai(message: str):
    return utils.get_emotion(message)