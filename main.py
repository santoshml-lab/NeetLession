
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    message: str
    type: str   # learn or solve


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
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


@app.post("/ai")
def ai_endpoint(data: UserInput):

    if data.type == "learn":

        system_prompt = """
You are an expert NEET teacher.

Generate the lesson using Markdown format.

Structure your response exactly like this:

# 📚 Topic Name

## 🧠 Concept Overview
Explain simply.

## 🔑 NEET Key Points
- Point 1
- Point 2
- Point 3

## ⚠ High Yield Facts
- Important Fact 1
- Important Fact 2

## 💡 Memory Trick
Provide an easy mnemonic.

## 📝 Quick Revision
2–3 line summary.

## 🎯 NEET Tip
Exam-oriented advice.

## ❓ Recall Questions
1. Question
2. Question
3. Question
"""

    elif data.type == "solve":

        system_prompt = """
You are a NEET expert problem solver.

Solve the question step-by-step.

Structure your answer using Markdown:

# 🧠 Solution

## 📌 Given

## ✏ Steps

## ✅ Final Answer

## 🎯 NEET Tip
"""

    else:

        return {
            "error": "Invalid type"
        }

    try:

        reply = call_groq(
            system_prompt,
            data.message
        )

        return {
            "reply": reply
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.get("/")
def home():

    return {
        "message": "NEET Hub API is running 🚀"
    }
