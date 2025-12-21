import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Analytics Dashboard", layout="wide", initial_sidebar_state="expanded")

# ----------------------------
# AUTHENTICATION
# ----------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Access denied. Please log in first.")
    st.stop()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.title("Dashboard Filters")
show_sample = st.sidebar.checkbox("Show CPU Sample Chart", value=True)
csv_filter = st.sidebar.multiselect("Select CSVs to visualize", [])

# ----------------------------
# HEADER & WELCOME
# ----------------------------
st.title("📊 Interactive Analytics Dashboard")
st.write(f"Hello, **{st.session_state.username}**, welcome to your dashboard!")

st.divider()

# ----------------------------
# TOP METRICS CARDS
# ----------------------------
st.subheader("Key Metrics Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Threats", 14, "+2")
with col2:
    st.metric("Incidents Closed", 32, "+5")
with col3:
    st.metric("Pending Tickets", 6, "-1")
with col4:
    st.metric("Open Cyber Incidents", 8, "+1")

st.divider()

# ----------------------------
# SAMPLE CPU USAGE CHART
# ----------------------------
if show_sample:
    st.subheader("Server CPU Usage (Sample)")
    cpu_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "CPU Usage (%)": [45, 55, 70, 60, 50]
    })
    st.line_chart(cpu_data.set_index("Day"))

# ----------------------------
# LOAD CSV FILES
# ----------------------------
base_dir = Path(__file__).parents[1]
csv_files = sorted(base_dir.glob("*.csv"))
data_dir = base_dir / "DATA"
if data_dir.exists():
    csv_files += sorted(data_dir.glob("*.csv"))

# Keep unique CSVs
csv_files = list(dict.fromkeys(csv_files))
if csv_filter:
    csv_files = [fp for fp in csv_files if fp.name in csv_filter]

# ----------------------------
# CSV VISUALIZATIONS
# ----------------------------
if csv_files:
    st.subheader("CSV Data Visualizations")
    for fp in csv_files:
        st.markdown(f"### {fp.name}")
        try:
            df = pd.read_csv(fp)
        except Exception as e:
            st.error(f"Failed to read {fp.name}: {e}")
            continue

        # ----------------------------
        # EXPANDABLE TABLE
        # ----------------------------
        with st.expander("Show Table Preview (10 rows)"):
            st.dataframe(df.head(10), use_container_width=True)

        # ----------------------------
        # SUMMARY STATISTICS
        # ----------------------------
        with st.expander("Summary Statistics"):
            st.dataframe(df.describe(include="all").transpose().fillna(""))

        # ----------------------------
        # INTERACTIVE CHARTS
        # ----------------------------
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        if numeric_cols:
            st.write("#### Interactive Charts")
            chart_tab_line, chart_tab_bar, chart_tab_area = st.tabs(["Line", "Bar", "Area"])

            # Dynamic x and y selection
            x_col = st.selectbox("Select X-axis column", options=cat_cols + numeric_cols, key=f"x_{fp.name}")
            y_col = st.selectbox("Select Y-axis column", options=numeric_cols, key=f"y_{fp.name}")

            # Line chart
            with chart_tab_line:
                if x_col and y_col:
                    try:
                        st.line_chart(df.set_index(x_col)[y_col])
                    except Exception:
                        st.info("Cannot plot line chart with selected columns.")

            # Bar chart
            with chart_tab_bar:
                if x_col and y_col:
                    try:
                        grouped = df.groupby(x_col)[y_col].sum()
                        st.bar_chart(grouped)
                    except Exception:
                        st.info("Cannot plot bar chart with selected columns.")

            # Area chart
            with chart_tab_area:
                if x_col and y_col:
                    try:
                        grouped = df.groupby(x_col)[y_col].sum()
                        st.area_chart(grouped)
                    except Exception:
                        st.info("Cannot plot area chart with selected columns.")

        else:
            st.info("No numeric columns available for charting.")

else:
    st.info("No CSV files found in project root or DATA folder.")

# ----------------------------
# ADDITIONAL ANALYTICS: IT Tickets
# ----------------------------
tickets_file = data_dir / "it_tickets.csv"
if tickets_file.exists():
    try:
        tickets = pd.read_csv(tickets_file, parse_dates=["created_date", "resolved_date"], infer_datetime_format=True)
        st.divider()
        st.subheader("IT Tickets Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Tickets by Priority")
            if "priority" in tickets.columns:
                counts = tickets["priority"].fillna("N/A").value_counts()
                st.bar_chart(counts)

        with col2:
            st.write("### Tickets Created per Month")
            if "created_date" in tickets.columns:
                tickets["created_date"] = pd.to_datetime(tickets["created_date"], errors="coerce")
                monthly = tickets.dropna(subset=["created_date"])
                monthly["month"] = monthly["created_date"].dt.to_period("M").astype(str)
                month_counts = monthly.groupby("month").size()
                st.line_chart(month_counts)

    except Exception as e:
        st.error(f"Error visualizing it_tickets.csv: {e}")
else:
    st.info("No DATA/it_tickets.csv file found.")