import argparse
import json


def handle_submission_event(event: dict) -> dict:
    submission_id = event.get("submission_id")
    if not submission_id:
        raise ValueError("submission_id is required")

    return {
        "submission_id": submission_id,
        "message": "Submission event converted into a processing request."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Local test for submission event function.")
    parser.add_argument("submission_id", help="Submission ID")
    args = parser.parse_args()

    result = handle_submission_event({"submission_id": args.submission_id})
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()