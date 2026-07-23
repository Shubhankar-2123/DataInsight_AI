import streamlit as st

from src.loader import load_dataset
from src.validator import validate_dataset
from src.profiler import get_dataset_overview

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="DataInsight AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Main Title
# --------------------------------------------------
st.title("📊 DataInsight AI")

# --------------------------------------------------
# Project Description
# --------------------------------------------------
st.markdown("""
### Smart Dataset Story Generator

Upload a **CSV** or **Excel** dataset to automatically:

- 📁 Explore the dataset
- 🔍 Check data quality
- 📈 Generate statistics
- 📊 Visualize trends
- 💡 Discover meaningful insights

Let's turn raw data into useful stories!
""")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("📁 Dataset Upload")
st.sidebar.markdown(
    "Upload a CSV or Excel file to begin your analysis."
)
st.sidebar.success("✅ Ready to analyze your dataset")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is None:
    st.info("👈 Please upload a CSV or Excel file to begin.")

else:
    try:
        # Loading dataset
        df = load_dataset(uploaded_file)
        st.success(f"Successfully loaded **{uploaded_file.name}**")

        # dataset validation
        is_valid, message = validate_dataset(df)

        if not is_valid:
            st.error(message)
            st.stop()

        st.success(message)

        st.success("Dataset loaded successfully!")

        overview_tab, quality_tab, statistics_tab, charts_tab, insights_tab = st.tabs(
            [
                "📋 Overview",
                "🧹 Data Quality",
                "📈 Statistics",
                "📊 Visualizations",
                "💡 Insights",
            ]
        )

        with overview_tab:
            # dataset overview
            overview = get_dataset_overview(df)
            st.subheader("📊 Dataset Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", overview["rows"])

            with col2:
                st.metric("Columns", overview["columns"])

            with col3:
                st.metric("Memory (MB)", overview["memory_usage"])

            col4, col5, col6 = st.columns(3)

            with col4:
                st.metric("Numeric", overview["numeric_columns"])

            with col5:
                st.metric("Categorical", overview["categorical_columns"])

            with col6:
                st.metric("Datetime", overview["datetime_columns"])

            # dataset preivew
            st.subheader("Dataset Preview")
            st.dataframe(df.head(), use_container_width=True)
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
        with quality_tab:
            st.subheader("🧹 Data Quality")
            st.info("This section will show missing values, duplicates, and other quality checks.")

        with statistics_tab:
            st.subheader("📈 Statistical Analysis")
            st.info("Statistical summaries will be displayed here.")

        with charts_tab:
            st.subheader("📊 Visualizations")
            st.info("Interactive charts will appear here.")            

        with insights_tab:
            st.subheader("💡 AI Insights")
            st.info("Automatically generated insights and stories will appear here.")
            
    except Exception as e:
            st.error(f"Error loading dataset: {e}")