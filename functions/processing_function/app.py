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

from functions.processing_function.handler import handle_processing
from shared.config import (
    get_function_headers,
    get_request_timeout,
    get_result_update_function_url,
)
from shared.function_security import verify_function_request
from shared.schemas import ProcessingRequest

app = FastAPI(title="Processing Function")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "processing-function"}


@app.post("/invoke")
def invoke(payload: ProcessingRequest, request: Request) -> dict:
    verify_function_request(request)

    processing_result = handle_processing(payload.submission_id)

    response = requests.post(
        get_result_update_function_url(),
        json=processing_result,
        headers=get_function_headers(),
        timeout=get_request_timeout(),
    )
    response.raise_for_status()

    return {
        "stage": "processing",
        "message": "Rules evaluated and forwarded to the result update function.",
        "processing_result": processing_result,
        "result_update_response": response.json(),
    }
