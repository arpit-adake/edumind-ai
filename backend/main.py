from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, session, chat

app = FastAPI(
    title="Chatbot API",
    description="Student Assistant + Code/Dev + Interview Prep",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(session.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
