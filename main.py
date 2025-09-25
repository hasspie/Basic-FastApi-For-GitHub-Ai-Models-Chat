from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN").strip().replace('"', '')
GITHUB_URL = "https://models.github.ai/inference/chat/completions"
MODEL = "openai/gpt-4.1"
app = FastAPI()

class UserPrompt(BaseModel):
    text: str

@app.post("/ask")
def ask(prompt: UserPrompt):
    
    user_text = prompt.text

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_text}],
    }

    response = requests.post(GITHUB_URL, headers=headers, json=data)
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]

    return {"answer": answer}
