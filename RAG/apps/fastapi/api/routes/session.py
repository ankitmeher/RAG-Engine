"""DELETE /session/{session_id} — purge all user data on logout."""

import os
import shutil

from fastapi import APIRouter, HTTPException

from RAG.shared.config.config import settings
from RAG.shared.db_layer import queries

router = APIRouter(prefix="/session", tags=["session"])


@router.delete("/{session_id}")
async def end_session(session_id: str):
    if not queries.session_exists(session_id):
        raise HTTPException(404, f"Session '{session_id}' not found.")

    deleted = queries.delete_session(session_id)

    # Remove uploaded files
    upload_path = os.path.join(settings.upload_dir, session_id)
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path)

    return {"session_id": session_id, "chunks_deleted": deleted, "status": "session ended"}
