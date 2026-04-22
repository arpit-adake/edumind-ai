import streamlit as st
from api_client import create_session, get_sessions, get_messages, send_message, delete_session
from auth_manager import load_token
load_token()

st.set_page_config(page_title="Interview Prep", page_icon="🎯", layout="wide")

if not st.session_state.get("token"):
    st.warning("Please login first from the home page.")
    st.stop()

st.title("🎯 Interview Prep")
st.caption("Mock interviews with detailed feedback and scoring.")

MODE = "interview"

with st.sidebar:
    st.header("Sessions")
    st.markdown("**Start a new interview:**")
    domain = st.selectbox("Domain", ["DSA", "System Design", "HR", "Full Stack", "Python", "Machine Learning"], key="domain_select")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="difficulty_select")
    num_questions = st.slider("Number of questions", min_value=3, max_value=10, value=5, key="num_questions")

    if st.button("Start Interview", type="primary", key="new_interview"):
        session = create_session(MODE, f"{domain} Interview")
        st.session_state.interview_session_id = session["id"]
        st.session_state.interview_messages = []
        st.session_state.interview_domain = domain
        st.session_state.interview_question_count = 0
        st.session_state.interview_scores = []
        st.session_state.interview_total = num_questions
        st.session_state.interview_active = True
        intro_prompt = f"Start a {difficulty} level {domain} mock interview with {num_questions} questions. Ask me the first question only. Do not give the answer yet."
        intro = send_message(session["id"], intro_prompt, MODE)
        st.session_state.interview_messages.append({"role": "assistant", "content": intro.get("reply", "")})
        st.session_state.interview_question_count = 1
        st.rerun()

    st.divider()
    sessions = get_sessions()
    interview_sessions = [s for s in sessions if s["mode"] == MODE]
    for s in interview_sessions:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(s["title"][:25], key=f"i_{s['id']}"):
                st.session_state.interview_session_id = s["id"]
                msgs = get_messages(s["id"])
                st.session_state.interview_messages = [
                    {"role": m["role"], "content": m["content"]} for m in msgs
                ]
                st.session_state.interview_active = False
                st.rerun()
        with col2:
            if st.button("Del", key=f"del_i_{s['id']}"):
                delete_session(s["id"])
                if st.session_state.get("interview_session_id") == s["id"]:
                    st.session_state.interview_session_id = None
                    st.session_state.interview_messages = []
                st.rerun()

    st.divider()
    st.markdown("**Tips:**")
    st.markdown("- Think out loud for DSA")
    st.markdown("- Use STAR method for HR")
    st.markdown("- Draw diagrams mentally for System Design")

if "interview_session_id" not in st.session_state:
    st.session_state.interview_session_id = None
if "interview_messages" not in st.session_state:
    st.session_state.interview_messages = []
if "interview_scores" not in st.session_state:
    st.session_state.interview_scores = []
if "interview_question_count" not in st.session_state:
    st.session_state.interview_question_count = 0
if "interview_total" not in st.session_state:
    st.session_state.interview_total = 5
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False

if not st.session_state.interview_session_id:
    st.info("Select a domain and click Start Interview to begin!")
else:
    if st.session_state.interview_active and st.session_state.interview_total > 0:
        progress = st.session_state.interview_question_count / st.session_state.interview_total
        st.progress(min(progress, 1.0), text=f"Question {min(st.session_state.interview_question_count, st.session_state.interview_total)} of {st.session_state.interview_total}")

        if st.session_state.interview_scores:
            avg_score = sum(st.session_state.interview_scores) / len(st.session_state.interview_scores)
            st.metric("Average Score So Far", f"{avg_score:.1f} / 10")

    for msg in st.session_state.interview_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if st.session_state.interview_active:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("End Interview & Get Summary", type="secondary", use_container_width=True):
                prompt = "The interview is now over. Please give me a comprehensive performance summary including: overall score, strengths, weaknesses, and specific areas to improve for each question answered."
                st.session_state.interview_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown("End Interview — requesting summary...")
                with st.chat_message("assistant"):
                    with st.spinner("Generating your performance report..."):
                        response = send_message(st.session_state.interview_session_id, prompt, MODE)
                        reply = response.get("reply", "Sorry, something went wrong.")
                        st.markdown(reply)
                st.session_state.interview_messages.append({"role": "assistant", "content": reply})
                st.session_state.interview_active = False
                st.rerun()

    if prompt := st.chat_input("Your answer..."):
        st.session_state.interview_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Evaluating your answer..."):
                response = send_message(st.session_state.interview_session_id, prompt, MODE)
                reply = response.get("reply", "Sorry, something went wrong.")
                st.markdown(reply)

                import re
                score_match = re.search(r'(\d+)\s*/\s*10', reply)
                if score_match:
                    st.session_state.interview_scores.append(int(score_match.group(1)))

        st.session_state.interview_messages.append({"role": "assistant", "content": reply})
        st.session_state.interview_question_count += 1