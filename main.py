import os
import re
import openai
from dotenv import load_dotenv

load_dotenv()

with open("prompts.txt", 'r') as f:
    out = f.read()

out = out.strip()

prompts = re.split(r'Prompt [0-9]:', out)[1:]
prompts = [re.sub('\n{2}', '\n', prompt) for prompt in prompts]

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def query_gpt(prompt, **kwargs):
    chat_completion = client.chat.completions.create(
        messages = [
            {
                'role': 'system',
                'content': prompt
            }
        ],
        model = 'gpt-4',
        **kwargs
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    responses = [query_gpt(p) for p in prompts]

    out = '  \n-------------------  \n'.join(responses)

    with open("output.txt", "w+") as f:
        f.write(out)