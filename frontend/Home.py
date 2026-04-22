import streamlit as st
from api_client import login, register, get_me
from auth_manager import save_token, load_token, clear_token

st.set_page_config(
    page_title="EduMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)
if not st.session_state.get("token"):
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)

def init_session():
    for key in ["token", "user", "session_id", "messages"]:
        if key not in st.session_state:
            st.session_state[key] = None

def get_me_with_token(token: str):
    import httpx
    r = httpx.get("http://localhost:8000/auth/me", headers={"Authorization": f"Bearer {token}"})
    return r.json()

init_session()
load_token()

if not st.session_state.get("sidebar_initialized"):
    st.session_state.sidebar_initialized = True
    st.query_params["sidebar"] = "collapsed"
if st.session_state.token and not st.session_state.user:
    try:
        st.session_state.user = get_me()
    except:
        st.session_state.token = None

if st.session_state.token and st.session_state.user:
    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.user['name']}**")
        st.divider()
        if st.button("Logout", type="secondary", use_container_width=True):
            clear_token()
            st.rerun()

    st.title("EduMind AI")
    st.success(f"Welcome back, {st.session_state.user['name']}!")
    st.markdown("Use the sidebar to navigate between modes.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📚 **Student Assistant**\nExplain concepts, summarize topics, generate quizzes")
        if st.button("Open Student Assistant", use_container_width=True, key="goto_student"):
            st.switch_page("pages/1_Student_Assistant.py")
    with col2:
        st.info("💻 **Code Assistant**\nDebug, explain, and generate code in any language")
        if st.button("Open Code Assistant", use_container_width=True, key="goto_code"):
            st.switch_page("pages/2_Code_Assistant.py")
    with col3:
        st.info("🎯 **Interview Prep**\nMock interviews with feedback and scoring")
        if st.button("Open Interview Prep", use_container_width=True, key="goto_interview"):
            st.switch_page("pages/3_Interview_Prep.py")
else:
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none; }
            .auth-container {
                max-width: 420px;
                margin: 0 auto;
                padding: 2rem;
            }
            .auth-title {
                font-size: 2.2rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }
            .auth-subtitle {
                font-size: 1rem;
                color: gray;
                margin-bottom: 2rem;
            }
            div[data-testid="stTextInput"] input {
                padding: 0.6rem 0.8rem;
                font-size: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.markdown("## 🤖 EduMind AI")
        st.markdown("Your all-in-one AI assistant for learning, coding, and interview prep.")
        st.divider()

        if st.session_state.auth_page == "login":
            st.markdown("### Welcome back")
            st.markdown("Sign in to your account")
            st.markdown("")

            email = st.text_input("Email address", key="login_email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Your password")
            st.markdown("")

            if st.button("Sign In", type="primary", use_container_width=True, key="login_btn"):
                if email and password:
                    data, status = login(email, password)
                    if status == 200:
                        user = get_me_with_token(data["access_token"])
                        save_token(data["access_token"], user)
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("")
            st.markdown("<div style='text-align:center'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("Create an account", use_container_width=True, key="goto_register"):
                st.session_state.auth_page = "register"
                st.rerun()

        elif st.session_state.auth_page == "register":
            st.markdown("### Create your account")
            st.markdown("Join EduMind AI for free")
            st.markdown("")

            name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
            email2 = st.text_input("Email address", key="reg_email", placeholder="you@example.com")
            password2 = st.text_input("Password", type="password", key="reg_password", placeholder="Create a password")
            st.markdown("")

            if st.button("Create Account", type="primary", use_container_width=True, key="reg_btn"):
                if name and email2 and password2:
                    data, status = register(name, email2, password2)
                    if status == 200:
                        st.success("Account created! Please sign in.")
                        st.session_state.auth_page = "login"
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Registration failed. Try again."))
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("")
            st.markdown("<div style='text-align:center'>Already have an account?</div>", unsafe_allow_html=True)
            if st.button("Sign in instead", use_container_width=True, key="goto_login"):
                st.session_state.auth_page = "login"
                st.rerun()

def get_me_with_token(token: str):
    import httpx
    r = httpx.get("http://localhost:8000/auth/me", headers={"Authorization": f"Bearer {token}"})
    return r.json()