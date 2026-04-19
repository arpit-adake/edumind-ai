from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# --- User schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Auth schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Session schemas ---
class SessionCreate(BaseModel):
    mode: str  # student | code | interview
    title: Optional[str] = None

class SessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    mode: str
    title: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Message schemas ---
class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Chat schemas ---
class ChatRequest(BaseModel):
    session_id: UUID
    message: str
    mode: str  # student | code | interview

class ChatResponse(BaseModel):
    reply: str
    session_id: UUID
    tokens_used: Optional[int] = None

# --- Interview schemas ---
class InterviewFeedback(BaseModel):
    question: str
    user_answer: str
    ai_feedback: str
    score: int
    domain: str

# --- Code snippet schemas ---
class CodeSnippetCreate(BaseModel):
    language: Optional[str] = None
    code: str

class CodeSnippetResponse(BaseModel):
    id: UUID
    language: Optional[str]
    code: str
    explanation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True