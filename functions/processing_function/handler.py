from pathlib import Path
import sys
import requests

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.constants import PROCESSING_DONE
from shared.schemas import ProcessingRequest, ProcessingResult
from functions.processing_function.rules import evaluate_submission

DATA_SERVICE_URL = "http://localhost:8002"


def handle_processing(submission_id: str) -> dict:
    response = requests.get(f"{DATA_SERVICE_URL}/submissions/{submission_id}", timeout=10)
    response.raise_for_status()
    record = response.json()

    result = evaluate_submission(record)
    result["submission_id"] = submission_id
    return result


if __name__ == "__main__":
    # Local manual test
    test_id = "replace-with-real-submission-id"
    print(handle_processing(test_id))