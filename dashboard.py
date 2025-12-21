import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Dashboard", layout="wide")

# -----------------------------
# ACCESS CONTROL
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.error("Access denied. Please log in first.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

# -----------------------------
# HEADER & SIGN OUT
# -----------------------------
st.title("📊 Dashboard")
st.success(f"Hello, {st.session_state.username}! You are now logged in.")
st.write("Welcome to your interactive dashboard area.")

st.divider()
if st.button("Sign Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been signed out.")
    st.switch_page("Home.py")

# -----------------------------
# LOAD CSV FILES
# -----------------------------
base_dir = Path(__file__).parents[1]
data_dir = base_dir / "DATA"

csv_files = sorted(base_dir.glob("*.csv"))
if data_dir.exists():
    csv_files += sorted(data_dir.glob("*.csv"))

# remove duplicates
seen = set()
csv_files = [p for p in csv_files if not (p in seen or seen.add(p))]

# Sidebar CSV filter
if csv_files:
    selected_csvs = st.sidebar.multiselect(
        "Select CSVs to display",
        options=[fp.name for fp in csv_files],
        default=[fp.name for fp in csv_files]
    )
    csv_files = [fp for fp in csv_files if fp.name in selected_csvs]

st.divider()
st.subheader("CSV Tables & Analytics")

# -----------------------------
# DISPLAY CSV FUNCTION
# -----------------------------
def display_csv(fp: Path):
    st.markdown(f"### 📄 {fp.name}")
    st.caption(str(fp))
    
    try:
        df = pd.read_csv(fp)
    except Exception as e:
        st.error(f"Failed to read {fp.name}: {e}")
        return

    # Expandable search/filter
    with st.expander("🔍 Filter / Search"):
        col_to_search = st.selectbox("Select column to search", df.columns.tolist(), key=f"search_col_{fp.name}")
        search_value = st.text_input("Filter value", key=f"search_val_{fp.name}")
        filtered_df = df[df[col_to_search].astype(str).str.contains(search_value, case=False, na=False)] if search_value else df

    # Tabs: Table / Summary / Charts
    tab_table, tab_summary, tab_chart = st.tabs(["Table", "Summary", "Charts"])

    with tab_table:
        st.dataframe(filtered_df.head(10), use_container_width=True)
        st.caption(f"First 10 rows — {len(filtered_df)} rows × {len(filtered_df.columns)} columns.")

    with tab_summary:
        try:
            st.dataframe(filtered_df.describe(include="all").transpose().fillna(""))
        except Exception:
            st.info("No summary available for this CSV.")

    with tab_chart:
        numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            chart_type = st.selectbox(
                "Chart Type",
                ["Line Chart", "Bar Chart", "Area Chart"],
                key=f"chart_type_{fp.name}"
            )
            y_col = st.selectbox("Select Y-axis", numeric_cols, key=f"chart_y_{fp.name}")
            x_col_options = filtered_df.columns.tolist()
            x_col = st.selectbox("Select X-axis", x_col_options, key=f"chart_x_{fp.name}")

            if chart_type == "Line Chart":
                st.line_chart(filtered_df.set_index(x_col)[y_col])
            elif chart_type == "Bar Chart":
                st.bar_chart(filtered_df.set_index(x_col)[y_col])
            elif chart_type == "Area Chart":
                st.area_chart(filtered_df.set_index(x_col)[y_col])
        else:
            st.info("No numeric columns available for charts.")

# -----------------------------
# DISPLAY ALL CSVS
# -----------------------------
if not csv_files:
    st.info("No CSV files found in project root or DATA/ folder.")
else:
    for fp in csv_files:
        display_csv(fp)
        st.divider()
