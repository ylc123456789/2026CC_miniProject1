import re
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.constants import (
    CATEGORY_ACADEMIC,
    CATEGORY_GENERAL,
    CATEGORY_OPPORTUNITY,
    CATEGORY_SOCIAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_NORMAL,
    PROCESSING_DONE,
    STATUS_APPROVED,
    STATUS_INCOMPLETE,
    STATUS_NEEDS_REVISION,
)


REQUIRED_FIELDS = ["title", "description", "location", "date", "organiser_name"]


def is_missing(value: str | None) -> bool:
    return value is None or str(value).strip() == ""


def detect_category(title: str | None, description: str | None) -> str:
    text = f"{title or ''} {description or ''}".lower()

    if any(word in text for word in ["career", "internship", "recruitment"]):
        return CATEGORY_OPPORTUNITY
    if any(word in text for word in ["workshop", "seminar", "lecture"]):
        return CATEGORY_ACADEMIC
    if any(word in text for word in ["club", "society", "social"]):
        return CATEGORY_SOCIAL
    return CATEGORY_GENERAL


def detect_priority(category: str) -> str:
    if category == CATEGORY_OPPORTUNITY:
        return PRIORITY_HIGH
    if category == CATEGORY_ACADEMIC:
        return PRIORITY_MEDIUM
    return PRIORITY_NORMAL


def evaluate_submission(record: dict) -> dict:
    for field in REQUIRED_FIELDS:
        if is_missing(record.get(field)):
            return {
                "final_status": STATUS_INCOMPLETE,
                "category": CATEGORY_GENERAL,
                "priority": PRIORITY_NORMAL,
                "note": f"Missing required field: {field}.",
                "processing_state": PROCESSING_DONE,
            }

    date_value = record.get("date", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
        category = detect_category(record.get("title"), record.get("description"))
        return {
            "final_status": STATUS_NEEDS_REVISION,
            "category": category,
            "priority": detect_priority(category),
            "note": "Date must be in YYYY-MM-DD format.",
            "processing_state": PROCESSING_DONE,
        }

    description = record.get("description", "") or ""
    if len(description.strip()) < 40:
        category = detect_category(record.get("title"), record.get("description"))
        return {
            "final_status": STATUS_NEEDS_REVISION,
            "category": category,
            "priority": detect_priority(category),
            "note": "Description must be at least 40 characters long.",
            "processing_state": PROCESSING_DONE,
        }

    category = detect_category(record.get("title"), record.get("description"))
    return {
        "final_status": STATUS_APPROVED,
        "category": category,
        "priority": detect_priority(category),
        "note": "Submission passed all required checks.",
        "processing_state": PROCESSING_DONE,
    }