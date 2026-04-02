"""POST /upload — accepts a PDF, assigns session_id, runs ingestion."""

import os
import shutil
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from RAG.shared.config.config import settings
from RAG.shared.ai_engine.ingestion import ingest_pdf

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("")
async def upload_pdf(
    file: UploadFile = File(...),
    session_id: str | None = None,
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only .pdf files are accepted.")

    session_id = session_id or str(uuid.uuid4())
    save_dir = os.path.join(settings.upload_dir, session_id)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)

    with open(file_path, "wb") as buf:
        shutil.copyfileobj(file.file, buf)

    try:
        summary = ingest_pdf(file_path=file_path, session_id=session_id)
    except Exception as exc:
        raise HTTPException(500, f"Ingestion failed: {exc}") from exc

    return {"session_id": session_id, **summary}
