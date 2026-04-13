from pathlib import Path
import sys
import json
import argparse
import requests

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from functions.processing_function.rules import evaluate_submission

DATA_SERVICE_URL = "http://localhost:8002"


def handle_processing(submission_id: str) -> dict:
    response = requests.get(f"{DATA_SERVICE_URL}/submissions/{submission_id}", timeout=10)
    response.raise_for_status()
    record = response.json()

    result = evaluate_submission(record)
    result["submission_id"] = submission_id
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Local test for processing function.")
    parser.add_argument("submission_id", help="Submission ID")
    args = parser.parse_args()

    result = handle_processing(args.submission_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()