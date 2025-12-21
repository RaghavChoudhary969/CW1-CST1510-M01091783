import streamlit as st
import json
import os

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Login", layout="centered")

USERS_FILE = "users.json"


# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------
def logout():
    """Clear session and log out the user."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()


def load_users():
    """Load users from JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}


def save_users(users):
    """Save users to JSON file."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


# ------------------------------------------------------------
# SESSION INITIALIZATION
# ------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------------------------------------------------
# LOAD USERS
# ------------------------------------------------------------
persistent_users = load_users()


# ------------------------------------------------------------
# CARD WRAPPER
# ------------------------------------------------------------
def card(content):
    st.markdown(
        f"""
        <div style="
            background: #f7f9fc;
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #e3e6ea;
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# IF LOGGED IN → SHOW LOGOUT CARD
# ------------------------------------------------------------
if st.session_state.logged_in:
    st.title("👋 Welcome Back!")
    card(f"""
        <h3 style="margin-bottom: 0;">Hello, {st.session_state.username}</h3>
        <p style="color: #666; margin-top: 8px;">
            You are already signed in.
        </p>
    """)

    if st.button("Log Out", use_container_width=True):
        logout()

    st.stop()


# ------------------------------------------------------------
# LOGIN & REGISTER TABS
# ------------------------------------------------------------
st.title("🔐 Authentication")

login_tab, register_tab = st.tabs(["Login", "Register"])

# ------------------------------------------------------------
# LOGIN TAB
# ------------------------------------------------------------
with login_tab:
    st.subheader("Sign In to Your Account")

    card("""
        <h4 style="margin-bottom: 15px;">Enter your login details</h4>
    """)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_btn = st.button("Sign In", use_container_width=True)

    if login_btn:
        if username in persistent_users and persistent_users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Incorrect username or password.")


# ------------------------------------------------------------
# REGISTER TAB
# ------------------------------------------------------------
with register_tab:
    st.subheader("Create a New Account")

    card("""
        <h4 style="margin-bottom: 15px;">Register a new profile</h4>
    """)

    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    reg_btn = st.button("Register", use_container_width=True)

    if reg_btn:
        if not new_user or not new_pass:
            st.warning("Please fill in all fields.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif new_user in persistent_users:
            st.error("Username already exists. Try another one.")
        else:
            persistent_users[new_user] = new_pass
            save_users(persistent_users)
            st.success("Account created! Switch to the Login tab to sign in.")
