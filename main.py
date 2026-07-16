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

# Request Model
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
        "model": "openai/gpt-oss-20b",
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
        system_prompt = (
            "You are an expert NEET teacher. "
            "Generate a complete NEET lesson in Markdown format."
        )

    elif data.type == "solve":
        system_prompt = (
            "You are a NEET expert problem solver. "
            "Give step-by-step solution."
        )

    elif data.type == "revision":
        system_prompt = (
            "You are a NEET revision expert. "
            "Generate short revision notes."
        )

    elif data.type == "mocktest":
        system_prompt = (
            "Generate exactly 10 NEET mock test MCQs with answers."
        )

    elif data.type == "mcq":
        system_prompt = (
            "Generate exactly 10 NEET MCQs with correct answers and explanations."
        )
    elif data.type == "dailychallenge":
        system_prompt = (
            "You are a NEET Daily Challenge Generator. "
            "Generate exactly 5 NEET MCQs. "
            "Mix Biology, Chemistry and Physics. "
            "For every question provide options, correct answer and explanation."
       )
    elif data.type == "studyplan":
        system_prompt = (
        "You are an expert NEET mentor. "
        "Generate a realistic 7-day NEET study plan. "
        "Include Physics, Chemistry, Biology, Revision and MCQ practice."
       )
        
    elif data.type == "ncertnotes":
        system_prompt = (
        "You are an expert Biology, Chemistry and Physics teacher for NEET. "
        "Generate completely original study notes in Markdown format. "
        "Do not copy or reproduce any textbook. "
        "Include:\n"
        "- Chapter Overview\n"
        "- Key Concepts\n"
        "- Important Definitions\n"
        "- Flowcharts\n"
        "- Tables\n"
        "- Memory Tricks\n"
        "- Important Points for Revision\n"
        "- Previous Exam Focus\n"
        "- 10 Practice MCQs with answers and explanations."
    )   
        
    elif data.type == "flashcards":
        system_prompt = (
        "You are an expert NEET teacher. "
        "Generate exactly 10 flashcards in Markdown format.\n\n"
        "Format:\n"
        "## Flashcard 1\n"
        "**Question:** ...\n"
        "**Answer:** ...\n\n"
        "Keep answers short and easy to revise."
    )  
        
    elif data.type == "quiz":
        system_prompt = (
        "You are an expert NEET examiner.\n"
        "Generate exactly 10 NEET multiple choice questions.\n\n"

        "Return ONLY plain text.\n"
        "No Markdown.\n"
        "No headings.\n"
        "No explanations.\n"
        "No extra text.\n\n"

        "Follow EXACTLY this format:\n\n"

        "Question 1: What is ...?\n"
        "A) Option A\n"
        "B) Option B\n"
        "C) Option C\n"
        "D) Option D\n"
        "Correct Answer: B\n\n"

        "Question 2: What is ...?\n"
        "A) Option A\n"
        "B) Option B\n"
        "C) Option C\n"
        "D) Option D\n"
        "Correct Answer: D\n\n"

        "Repeat this format until Question 10."
    )
        
    elif data.type == "analysis":
        system_prompt = (
        "You are an expert NEET mentor. "
        "Analyze the student's performance. "
        "Identify weak subjects, strong subjects, common mistakes, "
        "and give a 7-day improvement strategy."
    )    

   

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

