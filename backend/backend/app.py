# app.py - FastAPI gateway for UTO
import uuid, time, os
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from director import Director
from memory import init_db, SessionStore
from observability import setup_logging, record_metric

setup_logging()
init_db()

app = FastAPI(title="Universal Task Orchestrator (UTO)")

director = Director(session_store=SessionStore())

class SubmitRequest(BaseModel):
    user_id: str = "anonymous"
    goal: str
    deadline: str | None = None
    prefer_short: bool = True

@app.post("/submit")
async def submit(req: SubmitRequest):
    session_id = str(uuid.uuid4())
    director.create_session(session_id, req.user_id, meta={"deadline": req.deadline})
    record_metric("submissions_total", 1)
    director.start_job(session_id, req.goal, req.user_id, req.prefer_short)
    return {"session_id": session_id, "status": "started", "message": "Task orchestration started"}

@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...), session_id: str = None):
    target = f"uploads/{session_id or 'unsession'}_{int(time.time())}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(target, "wb") as f:
        f.write(await file.read())
    director.enqueue_document(session_id or "default", target)
    return {"status": "uploaded", "file": target}

@app.get("/status/{session_id}")
def status(session_id: str):
    state = director.get_session_status(session_id)
  return {"session_id": session_id, "state": state}

@app.get("/health")
def health():
    return {"status": "ok"}
