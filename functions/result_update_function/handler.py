import argparse
import json
import os
from pathlib import Path
import sys

import requests

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

DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://localhost:8002")


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


def handle_result_update_from_submission_id(submission_id: str) -> dict:
    result = handle_processing(submission_id)
    return handle_result_update(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local test for result update function.")
    parser.add_argument("submission_id", help="Submission ID")
    args = parser.parse_args()

    updated_record = handle_result_update_from_submission_id(args.submission_id)
    print(json.dumps(updated_record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
