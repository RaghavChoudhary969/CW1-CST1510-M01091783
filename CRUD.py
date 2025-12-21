import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="CRUD Dashboard", layout="wide")

# -----------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------
if not st.session_state.get("logged_in", False):
    st.error("Access denied. Please sign in.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("🛠 CRUD Dashboard")
st.write("Manage incidents, tickets, and cyber incidents interactively.")

# -----------------------------------------------------------
# PATHS
# -----------------------------------------------------------
base_dir = Path(__file__).parents[1]
data_dir = base_dir / "DATA"
data_dir.mkdir(exist_ok=True)

incidents_db = data_dir / "incidents.db"
cyber_db = data_dir / "cyber_incidents.db"
tickets_csv = data_dir / "it_tickets.csv"

# -----------------------------------------------------------
# DATABASE FUNCTIONS
# -----------------------------------------------------------
def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            severity TEXT,
            status TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_record(db_path, title, severity, status):
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO cyber_incidents (title, severity, status) VALUES (?,?,?)",
        (title, severity, status)
    )
    conn.commit()
    conn.close()


def delete_record(db_path, record_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM cyber_incidents WHERE id=?", (record_id,))
    conn.commit()
    removed = c.rowcount
    conn.close()
    return removed


def fetch_latest(db_path, limit=10):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(
            f"SELECT id, title, severity, status FROM cyber_incidents ORDER BY id DESC LIMIT {limit}",
            conn
        )
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# -----------------------------------------------------------
# CSV FUNCTIONS
# -----------------------------------------------------------
def ensure_csv(csv_path):
    if not csv_path.exists():
        pd.DataFrame(columns=["id", "title", "severity", "status"]).to_csv(csv_path, index=False)


def add_ticket(title, severity, status):
    ensure_csv(tickets_csv)
    df = pd.read_csv(tickets_csv)
    next_id = (df["id"].max() or 0) + 1
    df.loc[len(df)] = [next_id, title, severity, status]
    df.to_csv(tickets_csv, index=False)


def delete_ticket(ticket_id):
    ensure_csv(tickets_csv)
    df = pd.read_csv(tickets_csv)
    before = len(df)
    df = df[df["id"] != ticket_id]
    df.to_csv(tickets_csv, index=False)
    return before - len(df)


def fetch_tickets(limit=10):
    ensure_csv(tickets_csv)
    df = pd.read_csv(tickets_csv)
    return df.tail(limit)


# -----------------------------------------------------------
# UI HELPERS
# -----------------------------------------------------------
def stat_card(label, value):
    st.markdown(f"""
        <div style="padding:15px; border-radius:12px; background:#f0f2f6; text-align:center;">
            <h3 style="margin-bottom:5px;">{value}</h3>
            <p style="color:grey; margin-top:0;">{label}</p>
        </div>
    """, unsafe_allow_html=True)


# -----------------------------
# STATS CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    stat_card("Incidents DB Exists", incidents_db.exists())
with col2:
    stat_card("Cyber Incidents DB Exists", cyber_db.exists())
with col3:
    stat_card("Tickets CSV Exists", tickets_csv.exists())

st.divider()

# -----------------------------
# TABS LAYOUT
# -----------------------------
tab_incidents, tab_tickets, tab_cyber, tab_all = st.tabs(
    ["📁 Incidents", "🎫 Tickets", "🛡 Cyber Incidents", "📋 All Data"]
)

# -----------------------------
# TAB: INCIDENTS
# -----------------------------
with tab_incidents:
    st.header("📁 Manage Incidents")
    with st.expander("➕ Add Incident"):
        title = st.text_input("Title", key="inc1")
        sev = st.selectbox("Severity", ["low", "medium", "high"], key="inc2")
        stat = st.selectbox("Status", ["open", "resolved", "closed"], key="inc3")
        if st.button("Add Incident"):
            insert_record(incidents_db, title, sev, stat)
            st.success("Incident added!")
            st.experimental_rerun()

    with st.expander("🗑 Delete Incident"):
        delid = st.number_input("ID to delete", min_value=1, step=1, key="inc_del")
        if st.button("Delete Incident"):
            removed = delete_record(incidents_db, delid)
            st.info(f"Removed: {removed}")
            st.experimental_rerun()

    st.subheader("Latest Incidents")
    st.dataframe(fetch_latest(incidents_db), use_container_width=True)

# -----------------------------
# TAB: TICKETS
# -----------------------------
with tab_tickets:
    st.header("🎫 Manage Tickets (CSV)")
    with st.expander("➕ Add Ticket"):
        t_title = st.text_input("Ticket Title", key="tic1")
        t_sev = st.selectbox("Severity", ["low", "medium", "high"], key="tic2")
        t_status = st.selectbox("Status", ["open", "closed"], key="tic3")
        if st.button("Add Ticket"):
            add_ticket(t_title, t_sev, t_status)
            st.success("Ticket added!")
            st.experimental_rerun()

    with st.expander("🗑 Delete Ticket"):
        tdel = st.number_input("Ticket ID", min_value=1, step=1, key="tic_del")
        if st.button("Delete Ticket"):
            removed = delete_ticket(tdel)
            st.info(f"Removed: {removed}")
            st.experimental_rerun()

    st.subheader("Latest Tickets")
    st.dataframe(fetch_tickets(), use_container_width=True)

# -----------------------------
# TAB: CYBER INCIDENTS
# -----------------------------
with tab_cyber:
    st.header("🛡 Cyber Incidents")
    with st.expander("➕ Add Cyber Incident"):
        title2 = st.text_input("Title", key="cy1")
        sev2 = st.selectbox("Severity", ["low", "medium", "high"], key="cy2")
        stat2 = st.selectbox("Status", ["open", "resolved", "closed"], key="cy3")
        if st.button("Add Cyber Incident"):
            insert_record(cyber_db, title2, sev2, stat2)
            st.success("Cyber Incident added!")
            st.experimental_rerun()

    with st.expander("🗑 Delete Cyber Incident"):
        delid2 = st.number_input("Cyber ID", min_value=1, step=1, key="cy_del")
        if st.button("Delete Cyber"):
            removed = delete_record(cyber_db, delid2)
            st.info(f"Removed: {removed}")
            st.experimental_rerun()

    st.subheader("Latest Cyber Incidents")
    st.dataframe(fetch_latest(cyber_db), use_container_width=True)

# -----------------------------
# TAB: ALL DATA
# -----------------------------
with tab_all:
    st.header("📋 Complete Data Overview")
    st.subheader("Incidents DB")
    st.dataframe(fetch_latest(incidents_db, limit=50), use_container_width=True)

    st.subheader("Cyber Incidents DB")
    st.dataframe(fetch_latest(cyber_db, limit=50), use_container_width=True)

    st.subheader("Tickets CSV")
    st.dataframe(fetch_tickets(limit=50), use_container_width=True)