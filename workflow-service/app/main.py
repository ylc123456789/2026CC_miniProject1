from pathlib import Path
import sys
import requests
from fastapi import FastAPI, HTTPException

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.schemas import SubmissionCreate, WorkflowSubmitResponse

DATA_SERVICE_URL = "http://localhost:8002"

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

    # Local stage: we only simulate event publishing here.
    return WorkflowSubmitResponse(
        submission_id=created["id"],
        processing_state=created["processing_state"],
        event_dispatched=False,
        message="Submission record created. Event publishing will be connected next.",
    )