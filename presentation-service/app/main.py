from pathlib import Path
import sys

import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

CURRENT_FILE = Path(__file__).resolve()
for candidate in [CURRENT_FILE.parents[i] for i in range(min(6, len(CURRENT_FILE.parents)))]:
    if (candidate / "shared").exists():
        ROOT_DIR = candidate
        break
else:
    ROOT_DIR = CURRENT_FILE.parents[min(2, len(CURRENT_FILE.parents) - 1)]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from shared.config import (
    get_data_service_url,
    get_request_timeout,
    get_result_refresh_seconds,
    get_workflow_service_url,
    is_cloud_mode,
)
from shared.constants import PROCESSING_PENDING

WORKFLOW_SERVICE_URL = get_workflow_service_url()
DATA_SERVICE_URL = get_data_service_url()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Presentation Service")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "presentation-service",
        "mode": "cloud" if is_cloud_mode() else "local",
    }


@app.get("/")
def form_page(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "mode": "Cloud" if is_cloud_mode() else "Local",
        },
    )


@app.post("/submit")
def submit_form(
    title: str = Form(""),
    description: str = Form(""),
    location: str = Form(""),
    date: str = Form(""),
    organiser_name: str = Form(""),
):
    payload = {
        "title": title,
        "description": description,
        "location": location,
        "date": date,
        "organiser_name": organiser_name,
    }

    response = requests.post(
        f"{WORKFLOW_SERVICE_URL}/submit",
        json=payload,
        timeout=get_request_timeout(),
    )
    response.raise_for_status()
    result = response.json()

    submission_id = result["submission_id"]
    return RedirectResponse(url=f"/results/{submission_id}", status_code=303)


@app.get("/results/{submission_id}")
def result_page(request: Request, submission_id: str):
    response = requests.get(
        f"{DATA_SERVICE_URL}/submissions/{submission_id}",
        timeout=get_request_timeout(),
    )
    response.raise_for_status()
    record = response.json()

    auto_refresh = record.get("processing_state") == PROCESSING_PENDING and is_cloud_mode()

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "request": request,
            "record": record,
            "auto_refresh": auto_refresh,
            "refresh_seconds": get_result_refresh_seconds(),
            "mode": "Cloud" if is_cloud_mode() else "Local",
        },
    )
