import httpx
import streamlit as st

BASE_URL = "http://localhost:8000"

def get_headers():
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"}

def register(name: str, email: str, password: str):
    r = httpx.post(f"{BASE_URL}/auth/register", json={"name": name, "email": email, "password": password})
    return r.json(), r.status_code

def login(email: str, password: str):
    r = httpx.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return r.json(), r.status_code

def get_me():
    r = httpx.get(f"{BASE_URL}/auth/me", headers=get_headers())
    return r.json()

def create_session(mode: str, title: str = None):
    r = httpx.post(f"{BASE_URL}/sessions/", json={"mode": mode, "title": title}, headers=get_headers())
    return r.json()

def get_sessions():
    r = httpx.get(f"{BASE_URL}/sessions/", headers=get_headers())
    return r.json()

def get_messages(session_id: str):
    r = httpx.get(f"{BASE_URL}/sessions/{session_id}/messages", headers=get_headers())
    return r.json()

def send_message(session_id: str, message: str, mode: str):
    r = httpx.post(
        f"{BASE_URL}/chat/",
        json={"session_id": session_id, "message": message, "mode": mode},
        headers=get_headers(),
        timeout=60.0
    )
    return r.json()

def delete_session(session_id: str):
    r = httpx.delete(f"{BASE_URL}/sessions/{session_id}", headers=get_headers())
    return r.status_code
