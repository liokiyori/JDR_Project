from openai import OpenAI
import os
from dotenv import load_dotenv
from .models import Conversation

load_dotenv()

key = os.getenv("openai_key")
client = OpenAI(api_key=key)

def get_previous_messages(user):
    conversation = Conversation.objects.filter(user=user).order_by('timestamp')
    messages = []
    for message in conversation:
        messages.append({"role": "user", "content": message.prompt})
        messages.append({"role": "assistant", "content": message.response})
    return messages

def response(user, prompt):
    previous_messages = get_previous_messages(user)
    messages = [
        {"role": "system", "content": "You are a Dungeon Master in a fantasy role-playing game."}
    ] + previous_messages + [
        {"role": "user", "content": prompt}
    ]
    reponse = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::Aa1BNNld",
        messages=messages,
        store=True,
        )
    return reponse.choices[0].message.content

    