import streamlit as st
from pathlib import Path

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Settings", layout="wide")

# -----------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------
if not st.session_state.get("logged_in", False):
    st.error("Access denied. Please log in first.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️ Application Settings")
st.caption("Manage your profile, profile picture, and system preferences.")

# -----------------------------------------------------------
# DARK-THEME CARD COMPONENT
# -----------------------------------------------------------
def card(content, width="100%"):
    st.markdown(
        f"""
        <div style="
            background: rgba(30,30,30,0.6);  /* dark semi-transparent */
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #444;
            width:{width};
            color: #fff;
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------
# TABS
# -----------------------------------------------------------
tab_profile, tab_picture, tab_system = st.tabs(["🧑‍💼 Profile", "🖼 Profile Picture", "🛠 System"])

# -----------------------------------------------------------
# TAB 1 — PROFILE
# -----------------------------------------------------------
with tab_profile:
    st.subheader("Profile Information")
    card(f"""
        <h3 style='margin-bottom:0'>{st.session_state.username}</h3>
        <p style='color:#bbb; margin-top:5px;'>Current Display Name</p>
    """)

    st.write("### Update Display Name")
    new_name = st.text_input("New Display Name", st.session_state.username)

    if st.button("Save Name", key="save_name"):
        if new_name.strip():
            st.session_state.username = new_name.strip()
            st.success("✅ Display name updated successfully!")
            st.rerun()
        else:
            st.warning("⚠ Name cannot be empty.")

# -----------------------------------------------------------
# TAB 2 — PROFILE PICTURE
# -----------------------------------------------------------
with tab_picture:
    st.subheader("Profile Picture")

    if "pfp" not in st.session_state:
        st.session_state.pfp = None

    if st.session_state.pfp:
        card("<center><h4>Your Current Picture</h4></center>")
        st.image(st.session_state.pfp, width=180)
    else:
        st.info("No profile picture uploaded yet.")

    st.write("### Upload New Picture")
    uploaded_pfp = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])

    if uploaded_pfp:
        st.session_state.pfp = uploaded_pfp.read()
        st.success("✅ Profile picture updated!")
        st.rerun()

    if st.button("Remove Profile Picture", key="remove_pfp"):
        st.session_state.pfp = None
        st.success("✅ Profile picture removed!")
        st.rerun()

# -----------------------------------------------------------
# TAB 3 — SYSTEM SETTINGS
# -----------------------------------------------------------
with tab_system:
    st.subheader("System Settings")
    card("""
        <h4 style='margin:0;'>Reset Session</h4>
        <p style='margin:5px 0; color:#bbb;'>This will log you out, clear all session data, and reset the application.</p>
    """)

    if st.button("Reset Session", key="reset_session"):
        st.session_state.clear()
        st.success("✅ Session reset. Please restart the application.")
        st.stop()

    st.divider()
    st.write("### Optional Features")
    st.info("Here you could add future settings like email update, theme toggle, or notification preferences.")
