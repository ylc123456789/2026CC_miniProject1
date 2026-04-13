from pathlib import Path
import sys
import json
import argparse
import requests

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from functions.processing_function.handler import handle_processing

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