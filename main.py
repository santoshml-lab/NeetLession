
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_credentials=True,
allow_methods=[""],
allow_headers=["*"],
)

class UserInput(BaseModel):
message: str
type: str

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
Generate a complete NEET lesson in Markdown format.
"""

elif data.type == "solve":

    system_prompt = """

You are a NEET expert problem solver.

Provide:

- Given

- Steps

- Formula Used

- Final Answer

- NEET Tip
  """
  
  elif data.type == "revision":
  
    system_prompt = """

You are a NEET revision expert.

Generate short revision notes with:

- Key Points

- Important Facts

- One Liners

- Memory Tricks
  """
  
  elif data.type == "mocktest":
  
    system_prompt = """

Generate exactly 10 NEET Mock Test MCQs.

For every question provide:
Question
A)
B)
C)
D)

Answer
"""

elif data.type == "mcq":

    system_prompt = """

Generate exactly 10 NEET MCQs.

For every question provide:

Q1.
Question

A)
B)
C)
D)

Correct Answer:
Explanation:

Repeat until Q10.
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
