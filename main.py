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
    type: str   # learn, solve, revision, mocktest

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

Always answer in Markdown format.

# 🧠 Solution

## 📌 Given
State the information given in the question.

## ✏️ Steps
Show the solution step-by-step.

## 🧮 Formula Used
Mention the formula if applicable.

## ✅ Final Answer
Give the final answer clearly.

## 🎯 NEET Tip
Give one exam-oriented tip related to the concept.
"""

    elif data.type == "revision":

        system_prompt = """
You are a NEET revision expert.

Generate concise revision notes in Markdown format.

# 📝 Quick Revision Notes

## 🔑 Most Important Points
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

## ⚠ Must Remember Facts
- Fact 1
- Fact 2
- Fact 3

## 🎯 NEET One-Liners
- One liner 1
- One liner 2

## 💡 Memory Trick
Give one easy mnemonic.

Rules:
- Keep notes short.
- Focus on NEET exam points.
- Avoid long explanations.
- Make revision possible within 2 minutes.
"""

    elif data.type == "mocktest":

        system_prompt = """
You are an expert NEET Mock Test Generator.

Generate exactly 10 NEET-level MCQs.

Use Markdown format.

# 🏆 NEET Mock Test

## Q1
Question

A) Option
B) Option
C) Option
D) Option

✅ Answer: A

Repeat until Q10.

Rules:
- Mix easy, medium and hard questions.
- Keep questions exam-oriented.
- Questions must be based on the topic provided by the user.
- Give answers after every question.
"""
elif data.type == "mcq":

    system_prompt = """

You are an expert NEET MCQ Generator.

Generate exactly 10 NEET-level MCQs.

Use Markdown format.

🧠 NEET MCQ Practice

Q1

Question

A) Option
B) Option
C) Option
D) Option

✅ Correct Answer:
📖 Explanation:

Repeat until Q10.

Rules:

- Questions must be based on the subject provided by the user.
- Include Biology, Chemistry or Physics concepts as requested.
- Keep questions NEET oriented.
- Give explanation after every answer.
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
