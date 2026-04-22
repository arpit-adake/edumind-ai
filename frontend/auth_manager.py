import streamlit as st
import os
import json

TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".auth_cache.json")

def save_token(token: str, user: dict):
    st.session_state.token = token
    st.session_state.user = user
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token, "user": user}, f)

def load_token():
    if st.session_state.get("token"):
        return st.session_state.token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                st.session_state.token = data.get("token")
                st.session_state.user = data.get("user")
                return st.session_state.token
        except:
            return None
    return None

def clear_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    for key in list(st.session_state.keys()):
        del st.session_state[key]