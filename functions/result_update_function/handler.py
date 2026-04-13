from pathlib import Path
import sys
import requests

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.schemas import ProcessingResult

DATA_SERVICE_URL = "http://localhost:8002"


def handle_result_update(result: dict) -> dict:
    submission_id = result["submission_id"]

    payload = {
        "final_status": result["final_status"],
        "category": result["category"],
        "priority": result["priority"],
        "note": result["note"],
        "processing_state": result["processing_state"],
    }

    response = requests.put(
        f"{DATA_SERVICE_URL}/submissions/{submission_id}/result",
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    sample = {
        "submission_id": "replace-with-real-submission-id",
        "final_status": "APPROVED",
        "category": "ACADEMIC",
        "priority": "MEDIUM",
        "note": "Submission passed all required checks.",
        "processing_state": "DONE",
    }
    print(handle_result_update(sample))