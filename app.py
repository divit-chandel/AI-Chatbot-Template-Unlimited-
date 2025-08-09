# introduction  // Author: Divit Chandel
description = """
- Version: 1.1
- Description: Complete Python Terminal Chatbot w/ OpenRouter_OpenAI with Multiple Models

It's the backbone template type thing for any AI project I build whether It's with n8n, a normal script or |
most importantly a full stack app specially a SaaS so It's all in one take code from here & modify to fit  |
my project. 
"""

# Libraries
from openai import OpenAI
from ai_models import list
from dotenv import load_dotenv
import os

# Initializing API, Client, History & Custom Instructions
load_dotenv()
client = OpenAI(  # Initialize the client
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY"), # Note: Change it with st.secrets in UI
)
chat_history = [ # Custom Instructions & Chat History
    {"role": "system", "content": """You're a Helpful chatbot that answers things in short and sweet."""
    } # Note: Expand the big string bit big data
]

# Main Function For Response
def workflow(prompt):
    chat_history.append({"role": "user", "content": prompt})

    # Try models in order
    for model in list.models:
        try:
            # Debug log
            print(f"[INFO] Trying model: {model}")  # Note: Remove when with UI

            response = client.chat.completions.create(
                model=model,
                messages=chat_history # type: ignore
            )

            bot_reply = response.choices[0].message.content
            chat_history.append({"role": "assistant", "content": bot_reply})
            return bot_reply  # ✅ success, stop trying further

        except Exception as e:
            print(f"[ERROR] Model {model} failed: {e}") # Note: Remove when with UI
            continue  # move to next model

    # If we exhausted all models
    return "Sorry, all of our models are unavailable at the moment." # Note: Replace with st.error with UI


# Main Loop
if __name__ == "__main__":
    # print description
    print(description)
    # main loop
    while True:
        # Asking for Input
        user_input = input("Enter your prompt here >> ")
        # Quitting system
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        # Printing Response
        print(workflow(user_input))
