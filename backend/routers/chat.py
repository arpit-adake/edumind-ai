from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from backend.database import get_db
from backend.models import Session as ChatSession, Message
from backend.schemas import ChatRequest, ChatResponse
from backend.groq_client import get_groq_response
from backend.routers.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(ChatSession).filter(
        ChatSession.id == request.session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    history = db.query(Message).filter(
        Message.session_id == request.session_id
    ).order_by(Message.created_at.asc()).all()

    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": request.message})

    user_msg = Message(
        session_id=request.session_id,
        role="user",
        content=request.message
    )
    db.add(user_msg)
    db.commit()

    result = get_groq_response(request.mode, messages)

    ai_msg = Message(
        session_id=request.session_id,
        role="assistant",
        content=result["content"],
        tokens_used=result["tokens_used"]
    )
    db.add(ai_msg)
    db.commit()

    return ChatResponse(
        reply=result["content"],
        session_id=request.session_id,
        tokens_used=result["tokens_used"]
    )
