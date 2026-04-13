import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException

CURRENT_FILE = Path(__file__).resolve()
for candidate in [CURRENT_FILE.parents[i] for i in range(min(6, len(CURRENT_FILE.parents)))]:
    if (candidate / "shared").exists():
        ROOT_DIR = candidate
        break
else:
    ROOT_DIR = CURRENT_FILE.parents[min(2, len(CURRENT_FILE.parents) - 1)]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.constants import PROCESSING_PENDING
from shared.schemas import SubmissionCreate, SubmissionRecord, ResultUpdate

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "submissions.db"

app = FastAPI(title="Data Service")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                location TEXT,
                date TEXT,
                organiser_name TEXT,
                processing_state TEXT NOT NULL,
                final_status TEXT,
                category TEXT,
                priority TEXT,
                note TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def row_to_record(row: sqlite3.Row) -> SubmissionRecord:
    return SubmissionRecord(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        location=row["location"],
        date=row["date"],
        organiser_name=row["organiser_name"],
        processing_state=row["processing_state"],
        final_status=row["final_status"],
        category=row["category"],
        priority=row["priority"],
        note=row["note"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "data-service"}


@app.post("/submissions", response_model=SubmissionRecord)
def create_submission(payload: SubmissionCreate) -> SubmissionRecord:
    now = datetime.utcnow().isoformat()
    submission_id = str(uuid.uuid4())

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO submissions (
                id, title, description, location, date, organiser_name,
                processing_state, final_status, category, priority, note,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                submission_id,
                payload.title,
                payload.description,
                payload.location,
                payload.date,
                payload.organiser_name,
                PROCESSING_PENDING,
                None,
                None,
                None,
                None,
                now,
                now,
            ),
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM submissions WHERE id = ?",
            (submission_id,),
        ).fetchone()

    return row_to_record(row)


@app.get("/submissions/{submission_id}", response_model=SubmissionRecord)
def get_submission(submission_id: str) -> SubmissionRecord:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM submissions WHERE id = ?",
            (submission_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    return row_to_record(row)


@app.put("/submissions/{submission_id}/result", response_model=SubmissionRecord)
def update_result(submission_id: str, payload: ResultUpdate) -> SubmissionRecord:
    now = datetime.utcnow().isoformat()

    with get_conn() as conn:
        existing = conn.execute(
            "SELECT * FROM submissions WHERE id = ?",
            (submission_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Submission not found")

        conn.execute(
            """
            UPDATE submissions
            SET processing_state = ?,
                final_status = ?,
                category = ?,
                priority = ?,
                note = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                payload.processing_state,
                payload.final_status,
                payload.category,
                payload.priority,
                payload.note,
                now,
                submission_id,
            ),
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM submissions WHERE id = ?",
            (submission_id,),
        ).fetchone()

    return row_to_record(row)
