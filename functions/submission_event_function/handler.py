from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


def handle_submission_event(event: dict) -> dict:
    submission_id = event.get("submission_id")
    if not submission_id:
        raise ValueError("submission_id is required")

    return {
        "submission_id": submission_id,
        "message": "Submission event converted into a processing request."
    }


if __name__ == "__main__":
    print(handle_submission_event({"submission_id": "example-id"}))