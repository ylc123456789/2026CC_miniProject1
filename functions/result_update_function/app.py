from pathlib import Path
import sys

from fastapi import FastAPI, Request

CURRENT_FILE = Path(__file__).resolve()
for candidate in [CURRENT_FILE.parents[i] for i in range(min(6, len(CURRENT_FILE.parents)))]:
    if (candidate / "shared").exists():
        ROOT_DIR = candidate
        break
else:
    ROOT_DIR = CURRENT_FILE.parents[min(2, len(CURRENT_FILE.parents) - 1)]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from functions.result_update_function.handler import handle_result_update
from shared.function_security import verify_function_request
from shared.schemas import ProcessingResult

app = FastAPI(title="Result Update Function")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "result-update-function"}


@app.post("/invoke")
def invoke(payload: ProcessingResult, request: Request) -> dict:
    verify_function_request(request)

    updated_record = handle_result_update(payload.model_dump())
    return {
        "stage": "result_update",
        "message": "Stored record updated with the computed result.",
        "updated_record": updated_record,
    }
