from pathlib import Path
import sys

import requests
from fastapi import BackgroundTasks, FastAPI, HTTPException

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
from functions.result_update_function.handler import handle_result_update
from functions.submission_event_function.handler import handle_submission_event
from shared.config import (
    get_data_service_url,
    get_function_headers,
    get_request_timeout,
    get_submission_event_function_url,
    is_cloud_mode,
)
from shared.schemas import SubmissionCreate, WorkflowSubmitResponse

app = FastAPI(title="Workflow Service")


DATA_SERVICE_URL = get_data_service_url()


def dispatch_submission_event_cloud(submission_id: str) -> None:
    try:
        response = requests.post(
            get_submission_event_function_url(),
            json={"submission_id": submission_id},
            headers=get_function_headers(),
            timeout=get_request_timeout(),
        )
        response.raise_for_status()
        print(f"[workflow-service] cloud dispatch succeeded for submission_id={submission_id}")
    except Exception as exc:  # pragma: no cover - logging path
        print(f"[workflow-service] cloud dispatch failed for submission_id={submission_id}: {exc}")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "workflow-service",
        "mode": "cloud" if is_cloud_mode() else "local",
    }


@app.post("/submit", response_model=WorkflowSubmitResponse)
def submit(payload: SubmissionCreate, background_tasks: BackgroundTasks) -> WorkflowSubmitResponse:
    response = requests.post(
        f"{DATA_SERVICE_URL}/submissions",
        json=payload.model_dump(),
        timeout=get_request_timeout(),
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to create submission record")

    created = response.json()
    submission_id = created["id"]

    if is_cloud_mode():
        background_tasks.add_task(dispatch_submission_event_cloud, submission_id)
        return WorkflowSubmitResponse(
            submission_id=submission_id,
            processing_state=created["processing_state"],
            event_dispatched=True,
            message="Submission created. Background processing has been dispatched to Alibaba Cloud Function Compute.",
        )

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
