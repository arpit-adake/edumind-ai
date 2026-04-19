import streamlit as st
from api_client import create_session, get_sessions, get_messages, send_message, delete_session

st.set_page_config(page_title="Student Assistant", page_icon="📚", layout="wide")

if not st.session_state.get("token"):
    st.warning("Please login first from the home page.")
    st.stop()

st.title("📚 Student Assistant")
st.caption("Ask me anything — I will explain, summarize, and quiz you!")

MODE = "student"

with st.sidebar:
    st.header("Sessions")
    if st.button("New Session", type="primary", key="new_student"):
        session = create_session(MODE, "Student Session")
        st.session_state.student_session_id = session["id"]
        st.session_state.student_messages = []
        st.rerun()

    sessions = get_sessions()
    student_sessions = [s for s in sessions if s["mode"] == MODE]
    for s in student_sessions:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(s["title"][:25], key=f"s_{s['id']}"):
                st.session_state.student_session_id = s["id"]
                msgs = get_messages(s["id"])
                st.session_state.student_messages = [
                    {"role": m["role"], "content": m["content"]} for m in msgs
                ]
                st.rerun()
        with col2:
            if st.button("Del", key=f"del_s_{s['id']}"):
                delete_session(s["id"])
                if st.session_state.get("student_session_id") == s["id"]:
                    st.session_state.student_session_id = None
                    st.session_state.student_messages = []
                st.rerun()

    st.divider()
    st.markdown("**Shortcuts:**")
    shortcut = st.selectbox("Quick prompts", [
        "None",
        "Explain this topic simply",
        "Summarize what we discussed",
        "Give me 5 key points",
        "Quiz me on this topic"
    ], key="student_shortcut")

if "student_session_id" not in st.session_state:
    st.session_state.student_session_id = None
if "student_messages" not in st.session_state:
    st.session_state.student_messages = []

if not st.session_state.student_session_id:
    st.info("Click New Session in the sidebar to start chatting!")
else:
    for msg in st.session_state.student_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📝 Quiz Me", use_container_width=True):
            prompt = "Generate 5 multiple choice questions based on what we have discussed so far. Show answers at the end."
            st.session_state.student_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Generating quiz..."):
                    response = send_message(st.session_state.student_session_id, prompt, MODE)
                    reply = response.get("reply", "Sorry, something went wrong.")
                    st.markdown(reply)
            st.session_state.student_messages.append({"role": "assistant", "content": reply})
            st.rerun()
    with col2:
        if st.button("📋 Summarize Topic", use_container_width=True):
            prompt = "Summarize everything we have discussed so far in clear bullet points."
            st.session_state.student_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Summarizing..."):
                    response = send_message(st.session_state.student_session_id, prompt, MODE)
                    reply = response.get("reply", "Sorry, something went wrong.")
                    st.markdown(reply)
            st.session_state.student_messages.append({"role": "assistant", "content": reply})
            st.rerun()
    with col3:
        if st.button("💡 Key Concepts", use_container_width=True):
            prompt = "List the 5 most important concepts from our conversation that I should remember."
            st.session_state.student_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Extracting concepts..."):
                    response = send_message(st.session_state.student_session_id, prompt, MODE)
                    reply = response.get("reply", "Sorry, something went wrong.")
                    st.markdown(reply)
            st.session_state.student_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    st.divider()

    if shortcut != "None":
        prompt = shortcut
        st.session_state.student_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(st.session_state.student_session_id, prompt, MODE)
                reply = response.get("reply", "Sorry, something went wrong.")
                st.markdown(reply)
        st.session_state.student_messages.append({"role": "assistant", "content": reply})
        st.session_state.student_shortcut = "None"
        st.rerun()

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.student_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(st.session_state.student_session_id, prompt, MODE)
                reply = response.get("reply", "Sorry, something went wrong.")
                st.markdown(reply)
        st.session_state.student_messages.append({"role": "assistant", "content": reply})