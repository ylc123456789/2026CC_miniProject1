import os
from pathlib import Path
import sys

import requests
from fastapi import FastAPI, HTTPException

CURRENT_FILE = Path(__file__).resolve()
for candidate in [CURRENT_FILE.parents[i] for i in range(min(6, len(CURRENT_FILE.parents)))]:
    if (candidate / "shared").exists():
        ROOT_DIR = candidate
        break
else:
    ROOT_DIR = CURRENT_FILE.parents[min(2, len(CURRENT_FILE.parents) - 1)]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.schemas import SubmissionCreate, WorkflowSubmitResponse
from functions.submission_event_function.handler import handle_submission_event
from functions.processing_function.handler import handle_processing
from functions.result_update_function.handler import handle_result_update

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://localhost:8002")

app = FastAPI(title="Workflow Service")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "workflow-service"}


@app.post("/submit", response_model=WorkflowSubmitResponse)
def submit(payload: SubmissionCreate) -> WorkflowSubmitResponse:
    response = requests.post(
        f"{DATA_SERVICE_URL}/submissions",
        json=payload.model_dump(),
        timeout=10,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to create submission record")

    created = response.json()
    submission_id = created["id"]

    try:
        event_result = handle_submission_event({"submission_id": submission_id})
        processing_result = handle_processing(event_result["submission_id"])
        updated_record = handle_result_update(processing_result)

        return WorkflowSubmitResponse(
            submission_id=updated_record["id"],
            processing_state=updated_record["processing_state"],
            event_dispatched=True,
            message="Submission created and processed automatically in local mode.",
        )

    except Exception as exc:
        return WorkflowSubmitResponse(
            submission_id=submission_id,
            processing_state=created["processing_state"],
            event_dispatched=False,
            message=f"Submission record created, but local auto-processing failed: {str(exc)}",
        )
