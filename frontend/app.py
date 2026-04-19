import streamlit as st
from api_client import login, register

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session():
    for key in ["token", "user", "session_id", "messages"]:
        if key not in st.session_state:
            st.session_state[key] = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

init_session()

if st.session_state.token:
    st.title("?? AI Chatbot Platform")
    st.success(f"Welcome back, {st.session_state.user['name']}!")
    st.markdown("Use the sidebar to navigate between modes.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("?? **Student Assistant**\nExplain concepts, summarize topics, generate quizzes")
    with col2:
        st.info("?? **Code Assistant**\nDebug, explain, and generate code in any language")
    with col3:
        st.info("?? **Interview Prep**\nMock interviews with feedback and scoring")
    st.divider()
    if st.button("Logout", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.title("?? AI Chatbot Platform")
    st.markdown("Your all-in-one AI assistant for learning, coding, and interview prep.")
    st.divider()
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary", key="login_btn"):
            if email and password:
                data, status = login(email, password)
                if status == 200:
                    st.session_state.token = data["access_token"]
                    from api_client import get_me
                    st.session_state.user = get_me()
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please fill in all fields")

    with tab2:
        st.subheader("Create Account")
        name = st.text_input("Full Name", key="reg_name")
        email2 = st.text_input("Email", key="reg_email")
        password2 = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register", type="primary", key="reg_btn"):
            if name and email2 and password2:
                data, status = register(name, email2, password2)
                if status == 200:
                    st.success("Account created! Please login.")
                else:
                    st.error(data.get("detail", "Registration failed"))
            else:
                st.warning("Please fill in all fields")
