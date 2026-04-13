from pathlib import Path
import sys

import requests
from fastapi import FastAPI, Request

CURRENT_FILE = Path(__file__).resolve()
for candidate in [CURRENT_FILE.parents[i] for i in range(min(6, len(CURRENT_FILE.parents)))]:
    if (candidate / "shared").exists():
        ROOT_DIR = candidate
        break
else:
    ROOT_DIR = CURRENT_FILE.parents[min(2, len(CURRENT_FILE.parents) - 1)]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from functions.submission_event_function.handler import handle_submission_event
from shared.config import (
    get_function_headers,
    get_processing_function_url,
    get_request_timeout,
)
from shared.function_security import verify_function_request
from shared.schemas import ProcessingRequest

app = FastAPI(title="Submission Event Function")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "submission-event-function"}


@app.post("/invoke")
def invoke(payload: ProcessingRequest, request: Request) -> dict:
    verify_function_request(request)

    event_result = handle_submission_event(payload.model_dump())

    response = requests.post(
        get_processing_function_url(),
        json=event_result,
        headers=get_function_headers(),
        timeout=get_request_timeout(),
    )
    response.raise_for_status()

    return {
        "stage": "submission_event",
        "message": "Submission event converted into a processing request and forwarded.",
        "processing_response": response.json(),
    }
