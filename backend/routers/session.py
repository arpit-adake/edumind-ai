from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from backend.database import get_db
from backend.models import Session as ChatSession, Message
from backend.schemas import SessionCreate, SessionResponse, MessageResponse
from backend.routers.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse)
def create_session(data: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.mode not in ["student", "code", "interview"]:
        raise HTTPException(status_code=400, detail="Mode must be student, code, or interview")
    session = ChatSession(
        user_id=current_user.id,
        mode=data.mode,
        title=data.title or f"{data.mode.capitalize()} Session"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.get("/", response_model=List[SessionResponse])
def get_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ChatSession).filter(ChatSession.user_id == current_user.id).order_by(ChatSession.created_at.desc()).all()

@router.get("/{session_id}/messages", response_model=List[MessageResponse])
def get_messages(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()

@router.delete("/{session_id}")
def delete_session(session_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"message": "Session deleted"}
