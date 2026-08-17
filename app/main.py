import os

import requests
from fastapi import FastAPI

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = "llama3.2:1b"


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL
    }


@app.post("/generate")
def generate(prompt: str):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return {
        "model": data["model"],
        "response": data["response"],
        "duration_ms": round(data["total_duration"] / 1_000_000)
    }