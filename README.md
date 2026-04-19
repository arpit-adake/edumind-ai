# EduMind AI — Multi-Mode Intelligent Chatbot

An AI-powered chatbot platform built with Streamlit, FastAPI, PostgreSQL, and Groq LLM (Llama 3.3 70B).

## Features
- Student Assistant — explain concepts, summarize topics, generate quizzes
- Code Assistant — debug, explain, and generate code in any language
- Interview Prep — mock interviews with scoring and performance reports

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Database: PostgreSQL (Supabase)
- LLM: Groq API (Llama 3.3 70B)
- Auth: JWT (python-jose)
- ORM: SQLAlchemy + Alembic

## Setup
1. Clone the repo
2. Create a virtual environment and install dependencies
3. Add your .env file with DATABASE_URL, GROQ_API_KEY, SECRET_KEY
4. Run migrations: alembic upgrade head
5. Start backend: uvicorn backend.main:app --reload
6. Start frontend: cd frontend && streamlit run app.py