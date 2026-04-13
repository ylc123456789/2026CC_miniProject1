from pathlib import Path
import sys
import requests

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

WORKFLOW_SERVICE_URL = "http://localhost:8001"
DATA_SERVICE_URL = "http://localhost:8002"

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Presentation Service")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "presentation-service"}


@app.get("/")
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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

    response = requests.post(f"{WORKFLOW_SERVICE_URL}/submit", json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()

    submission_id = result["submission_id"]
    return RedirectResponse(url=f"/results/{submission_id}", status_code=303)


@app.get("/results/{submission_id}")
def result_page(request: Request, submission_id: str):
    response = requests.get(f"{DATA_SERVICE_URL}/submissions/{submission_id}", timeout=10)
    response.raise_for_status()
    record = response.json()

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "record": record,
        },
    )