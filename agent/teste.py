import os
from mistralai import Mistral
from model.env import Env
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)
print(chat_response.choices[0].message.content)