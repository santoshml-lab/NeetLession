from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class UserInput(BaseModel):
    message: str
    type: str  # "learn" or "solve"


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def call_groq(system_prompt, user_message):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()["choices"][0]["message"]["content"]


@app.post("/ai")
def ai_endpoint(data: UserInput):

    # Learn Mode
    if data.type == "learn":

        system_prompt = (
            "You are an expert NEET teacher. "
            "Explain topics in simple language with exam-focused notes, examples and clarity."
        )

    # Solve Mode
    elif data.type == "solve":

        system_prompt = (
            "You are a NEET expert problem solver. "
            "Give step-by-step solution with clear explanation and final answer."
        )

    else:

        return {"error": "Invalid type"}

    reply = call_groq(system_prompt, data.message)

    return {
        "reply": reply
    }
