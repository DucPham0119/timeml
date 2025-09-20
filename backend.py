# backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional

from models.gemini_event import tag_event_gemini
from models.gemini_time import tag_timex3_gemini
from models.our_model import time_model, event_model
import subprocess

app = FastAPI(title="Temporal & Event Extraction API")


# -----------------------------
# Request model
# -----------------------------
class ExtractionRequest(BaseModel):
    text: str
    time_model: Optional[Literal["", "GPT", "Gemini", "Heidel-Time", "Our-Model"]]
    event_model: Optional[Literal["", "GPT", "Gemini", "Our-Model"]]


# -----------------------------
# Utility functions
# -----------------------------
def run_heideltime(text: str) -> str:
    """Gọi HeidelTime qua subprocess"""
    try:
        result = subprocess.run(
            ["java", "-jar", "heideltime/heideltime.jar", "-text", text, "-l", "VIETNAMESE"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        return result.stdout
    except Exception as e:
        raise RuntimeError(f"HeidelTime error: {e}")


def run_time_model(model: str, text: str) -> str:
    if model == "GPT":
        return ""  # placeholder
    elif model == "Gemini":
        return tag_timex3_gemini(text)  # placeholder
    elif model == "Our-Model":
        return ""
        # return time_model.extract_time(text)
    elif model == "Heidel-Time":
        return ""
        # return run_heideltime(text)
    else:
        raise ValueError(f"Unknown time model: {model}")


def run_event_model(model: str, text: str) -> str:
    if model == "GPT":
        return ""  # placeholder
    elif model == "Gemini":
        return tag_event_gemini(text)
    elif model == "Our-Model":
        return event_model.event_pipeline(text)
    else:
        raise ValueError(f"Unknown event model: {model}")


def process_request(text: str, model_time: Optional[str], model_event: Optional[str]):
    time_result = run_time_model(model_time, text) if model_time else None
    event_result = run_event_model(model_event, text) if model_event else None
    return {
        "text": text,
        "time": time_result,
        "event": event_result
    }


# -----------------------------
# API endpoints
# -----------------------------
@app.get("/")
async def root():
    return {"message": "Temporal & Event Extraction API is running"}


@app.post("/extract")
async def extract(req: ExtractionRequest):
    try:
        result = process_request(req.text, req.time_model, req.event_model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
