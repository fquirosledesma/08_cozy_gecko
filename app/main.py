import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

API_VERSION = "0.2.0"

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
).rstrip("/")

MODEL = os.getenv(
    "MODEL",
    "llama3.2:1b"
)

REQUEST_TIMEOUT_SECONDS = float(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "120")
)

MAX_PROMPT_LENGTH = int(
    os.getenv("MAX_PROMPT_LENGTH", "4000")
)

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(
    title="Cozy Gecko API",
    description="Portable API for local generative AI with Ollama.",
    version=API_VERSION,
    default_response_class=UTF8JSONResponse
)


class GenerateRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        max_length=MAX_PROMPT_LENGTH,
        description="Instruction sent to the configured language model."
    )


class GenerateResponse(BaseModel):
    model: str
    response: str
    duration_ms: int | None = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "cozy-gecko-api",
        "version": API_VERSION
    }


@app.get("/ready")
def ready():
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=5
        )
        response.raise_for_status()

        models = [
            model.get("name")
            for model in response.json().get("models", [])
        ]

        if MODEL not in models:
            raise HTTPException(
                status_code=503,
                detail=f"Configured model '{MODEL}' is not available."
            )

        return {
            "status": "ready",
            "model": MODEL
        }

    except HTTPException:
        raise
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not available."
        )


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(
            status_code=422,
            detail="Prompt cannot be empty."
        )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        data = response.json()

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="The model took too long to respond."
        )
    except requests.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not available."
        )
    except requests.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Ollama rejected the generation request."
        )
    except (requests.RequestException, ValueError):
        raise HTTPException(
            status_code=502,
            detail="Invalid response received from Ollama."
        )

    duration = data.get("total_duration")

    return {
        "model": data.get("model", MODEL),
        "response": data.get("response", ""),
        "duration_ms": (
            round(duration / 1_000_000)
            if isinstance(duration, (int, float))
            else None
        )
    }