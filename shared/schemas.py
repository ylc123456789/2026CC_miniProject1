from datetime import datetime
from pydantic import BaseModel, Field


class SubmissionCreate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    date: str | None = None
    organiser_name: str | None = None


class SubmissionRecord(BaseModel):
    id: str
    title: str | None = None
    description: str | None = None
    location: str | None = None
    date: str | None = None
    organiser_name: str | None = None

    processing_state: str
    final_status: str | None = None
    category: str | None = None
    priority: str | None = None
    note: str | None = None

    created_at: str
    updated_at: str


class ResultUpdate(BaseModel):
    final_status: str
    category: str
    priority: str
    note: str
    processing_state: str


class WorkflowSubmitResponse(BaseModel):
    submission_id: str
    processing_state: str
    event_dispatched: bool = False
    message: str = ""


class ProcessingRequest(BaseModel):
    submission_id: str


class ProcessingResult(BaseModel):
    submission_id: str
    final_status: str
    category: str
    priority: str
    note: str
    processing_state: str