import streamlit as st
from api_client import create_session, get_sessions, get_messages, send_message, delete_session
from auth_manager import load_token
load_token()

st.set_page_config(page_title="Code Assistant", page_icon="💻", layout="wide")

if not st.session_state.get("token"):
    st.warning("Please login first from the home page.")
    st.stop()

st.title("💻 Code Assistant")
st.caption("Debug, explain, and generate code in any language.")

MODE = "code"

LANGUAGES = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "SQL", "Bash", "Other"]

with st.sidebar:
    st.header("Sessions")
    if st.button("New Session", type="primary", key="new_code"):
        session = create_session(MODE, "Code Session")
        st.session_state.code_session_id = session["id"]
        st.session_state.code_messages = []
        st.rerun()

    sessions = get_sessions()
    code_sessions = [s for s in sessions if s["mode"] == MODE]
    for s in code_sessions:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(s["title"][:25], key=f"c_{s['id']}"):
                st.session_state.code_session_id = s["id"]
                msgs = get_messages(s["id"])
                st.session_state.code_messages = [
                    {"role": m["role"], "content": m["content"]} for m in msgs
                ]
                st.rerun()
        with col2:
            if st.button("Del", key=f"del_c_{s['id']}"):
                delete_session(s["id"])
                if st.session_state.get("code_session_id") == s["id"]:
                    st.session_state.code_session_id = None
                    st.session_state.code_messages = []
                st.rerun()

    st.divider()
    st.markdown("**Language**")
    selected_lang = st.selectbox("Select language", LANGUAGES, key="code_language")

    st.divider()
    st.markdown("**Quick Actions**")
    quick_action = st.selectbox("Action", [
        "None",
        "Explain this code",
        "Find bugs in this code",
        "Optimize this code",
        "Add comments to this code",
        "Write unit tests for this code"
    ], key="code_action")

if "code_session_id" not in st.session_state:
    st.session_state.code_session_id = None
if "code_messages" not in st.session_state:
    st.session_state.code_messages = []

if not st.session_state.code_session_id:
    st.info("Click New Session in the sidebar to start chatting!")
else:
    for msg in st.session_state.code_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    with st.expander("Paste & Debug — paste your code here for instant analysis"):
        paste_lang = st.selectbox("Language", LANGUAGES, key="paste_lang")
        pasted_code = st.text_area("Paste your code", height=200, key="pasted_code", placeholder="Paste your code here...")
        paste_action = st.selectbox("What do you want?", [
            "Debug and fix errors",
            "Explain line by line",
            "Optimize for performance",
            "Add proper comments",
            "Write unit tests"
        ], key="paste_action_select")
        if st.button("Analyze Code", type="primary", key="analyze_btn"):
            if pasted_code.strip():
                prompt = f"Here is my {paste_lang} code:\n\n```{paste_lang.lower()}\n{pasted_code}\n```\n\nPlease: {paste_action}"
                st.session_state.code_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(f"Analyzing {paste_lang} code — {paste_action}")
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing..."):
                        response = send_message(st.session_state.code_session_id, prompt, MODE)
                        reply = response.get("reply", "Sorry, something went wrong.")
                        st.markdown(reply)
                st.session_state.code_messages.append({"role": "assistant", "content": reply})
                st.rerun()
            else:
                st.warning("Please paste some code first.")

    st.divider()

    if quick_action != "None":
        prompt = f"In {selected_lang}: {quick_action}"
        st.session_state.code_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Working on it..."):
                response = send_message(st.session_state.code_session_id, prompt, MODE)
                reply = response.get("reply", "Sorry, something went wrong.")
                st.markdown(reply)
        st.session_state.code_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if prompt := st.chat_input(f"Ask me about {selected_lang} code..."):
        full_prompt = f"[{selected_lang}] {prompt}"
        st.session_state.code_messages.append({"role": "user", "content": full_prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Coding..."):
                response = send_message(st.session_state.code_session_id, full_prompt, MODE)
                reply = response.get("reply", "Sorry, something went wrong.")
                st.markdown(reply)
        st.session_state.code_messages.append({"role": "assistant", "content": reply})