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

    try:
        with open(file_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        # Process the PDF into the vector store
        summary = ingest_pdf(file_path=file_path, session_id=session_id)
        
    except Exception as exc:
        raise HTTPException(500, f"Ingestion failed: {exc}") from exc
        
    finally:
        # CLEANUP: Delete the local file and directory immediately
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                # Remove the session directory if empty
                if os.path.exists(save_dir) and not os.listdir(save_dir):
                    os.rmdir(save_dir)
                print(f"--- [CLEANUP] Deleted local file: {file_path} ---")
            except Exception as e:
                print(f"--- [CLEANUP] Warning: Could not delete {file_path}: {e} ---")

    return {"session_id": session_id, **summary}
