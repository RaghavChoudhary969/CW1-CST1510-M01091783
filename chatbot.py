import streamlit as st
from openai import OpenAI

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Operations Console",
    page_icon="🧠",
    layout="wide"
)

# ---------------- Auth Check ----------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

# ---------------- Safe Defaults ----------------
st.session_state.setdefault("username", "Unknown")
st.session_state.setdefault("role", "user")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("selected_domain", "Cybersecurity")

# ---------------- OpenAI Client ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- System Prompts ----------------
DOMAIN_PROMPTS = {
    "Cybersecurity": "You are a cybersecurity expert assistant.",
    "Data Science": "You are a data science expert assistant.",
    "IT Operations": "You are an IT operations expert assistant."
}

# ================= TOP CONTROL BAR =================
top_left, top_mid, top_right = st.columns([3, 4, 3])

with top_left:
    st.markdown("### 🧠 AI Operations Console")
    st.caption("Multi-Domain Intelligence Platform")

with top_mid:
    st.session_state.selected_domain = st.selectbox(
        "Domain",
        list(DOMAIN_PROMPTS.keys()),
        index=list(DOMAIN_PROMPTS.keys()).index(st.session_state.selected_domain),
        label_visibility="collapsed"
    )

with top_right:
    st.markdown(f"👤 *{st.session_state.username}*")
    st.markdown(f"🔑 ⁠ {st.session_state.role.upper()} ⁠")

st.divider()

# ================= MAIN LAYOUT =================
left_panel, chat_panel = st.columns([2, 5])

# ---------------- LEFT PANEL ----------------
with left_panel:
    st.subheader("⚙️ Session Controls")

    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0
    )

    temperature = st.slider(
        "Creativity Level",
        0.0, 2.0, 1.0, 0.1
    )

    st.markdown("#### 📌 Active System Prompt")
    st.info(DOMAIN_PROMPTS[st.session_state.selected_domain])

    st.markdown("---")

    if st.button("🗑 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.metric(
        "Conversation Turns",
        len([m for m in st.session_state.messages if m["role"] != "system"])
    )

# ---------------- CHAT PANEL ----------------
with chat_panel:
    st.subheader("💬 AI Workspace")

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input box
    user_input = st.chat_input(
        f"Ask something in {st.session_state.selected_domain}..."
    )

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Prepare full conversation with system prompt at top
        messages_payload = [
            {"role": "system", "content": DOMAIN_PROMPTS[st.session_state.selected_domain]}
        ] + st.session_state.messages

        # Generate AI reply
        with st.spinner("AI is processing..."):
            response = client.chat.completions.create(
                model=model,
                messages=messages_payload,
                temperature=temperature
            )

        assistant_reply = response.choices[0].message.content.strip()

        # Show assistant reply
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_reply
        })
