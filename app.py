import streamlit as st

from src.loader import load_dataset

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

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is None:
    st.info("👈 Please upload a CSV or Excel file to begin.")

else:
    try:
        df = load_dataset(uploaded_file)

        st.success("Dataset loaded successfully!")

        st.subheader("Dataset Preview")

        st.dataframe(df.head())
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")

    except Exception as e:
        st.error(f"Error loading dataset: {e}")