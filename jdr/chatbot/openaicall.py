from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("openai_key")
client = OpenAI(api_key=key)

def response(prompt):
    reponse = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
            ]
        )
    return reponse.choices[0].message.content