import streamlit as st
import pandas as pd

from src.loader import load_dataset
from src.validator import validate_dataset
from src.profiler import get_dataset_overview
from src.quality import analyze_data_quality
from src.statistics import generate_statistics
from src.visualization import (
    create_histogram,
    create_boxplot,
    create_correlation_heatmap,
    create_scatter_plot,
    create_bar_chart,
    create_line_chart,
    detect_datetime_columns,
)

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
            st.dataframe(df.head(), width='stretch')
            st.write(f"**File Name:** {uploaded_file.name}")
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
        with quality_tab:
            quality = analyze_data_quality(df)
            st.subheader("🧹 Data Quality")
            

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Missing Values",
                    int(quality["missing_values"].sum())
                )

            with col2:
                st.metric(
                    "Duplicate Rows",
                    quality["duplicate_rows"]
                )

            st.divider()
            missing_df = quality["missing_values"]

            missing_df = missing_df[missing_df > 0]

            if not missing_df.empty:

                st.write("### Missing Values by Column")

                st.dataframe(
                    missing_df.rename("Missing Count")
                )

            else:

                st.success("✅ No missing values found.")

            if quality["empty_columns"]:

                st.warning("### Empty Columns")

                st.write(quality["empty_columns"])

            else:

                st.success("✅ No empty columns.")

            if quality["constant_columns"]:

                st.warning("### Constant Columns")

                constant_df = pd.DataFrame(
                    {"Column Name": quality["constant_columns"]}
                )

                st.dataframe(constant_df, width=True)

            else:

                st.success("✅ No constant columns.")

        with statistics_tab:
            statistics_df = generate_statistics(df)
            st.subheader("📈 Statistical Analysis")
        
            
            if statistics_df.empty:

                st.warning("No numeric columns found in the dataset.")

            else:
                st.metric(
                "Numeric Columns Analysed",
                statistics_df.shape[0]
                )

                st.dataframe(
                    statistics_df,
                    width='stretch'
                )

        with charts_tab:
            
            st.subheader("📊 Visualizations")
            numeric_columns = df.select_dtypes(include="number").columns
            selected_column = st.selectbox(
                "Select Numeric Column",
                numeric_columns
            )

            st.subheader("📈 Histogram")
            histogram = create_histogram(
                df,
                selected_column
            )

            st.plotly_chart(
                histogram,
                width='stretch',
                key="histogram"
            )


            st.subheader("📦 Box Plot")
            box_plot = create_boxplot(
                df,
                selected_column
            )

            st.plotly_chart(
                box_plot,
                width="stretch",
                key="boxplot"
            )

            st.subheader("🔥 Correlation Heatmap")

            heatmap = create_correlation_heatmap(df)

            if heatmap:
                st.plotly_chart(
                    heatmap,
                    width="stretch",
                    key="heatmap"
                )
            else:
                st.info("Need at least two numeric columns to generate a correlation heatmap.")
            st.subheader("📈 Scatter Plot")

            numeric_columns = df.select_dtypes(include="number").columns.tolist()

            if len(numeric_columns) >= 2:

                col1, col2 = st.columns(2)

                with col1:
                    x_column = st.selectbox(
                        "X-Axis",
                        numeric_columns,
                        key="scatter_x"
                    )

                with col2:
                    y_column = st.selectbox(
                        "Y-Axis",
                        numeric_columns,
                        index=1,
                        key="scatter_y"
                    )
                
                if x_column == y_column:
                    st.warning("Please select two different columns.")
                else:
                   

                    scatter = create_scatter_plot(
                        df,
                        x_column,
                        y_column
                    )

                    st.plotly_chart(
                        scatter,
                        width="stretch",
                        key="scatter"
                    )

            else:
                st.info("Need at least two numeric columns for a scatter plot.")


            st.subheader("📊 Categorical Distribution")

            categorical_columns = (
                df.select_dtypes(
                    include=["object", "string", "category"]
                ).columns.tolist()
            )

            if categorical_columns:

                selected_category = st.selectbox(
                    "Select Categorical Column",
                    categorical_columns,
                    key="bar_chart"
                )

                bar_fig = create_bar_chart(
                    df,
                    selected_category
                )

                st.plotly_chart(
                    bar_fig,
                    width="stretch",
                    key="bar"
                )

            else:
                st.info("No categorical columns found.")
            
            datetime_columns = detect_datetime_columns(df)

            st.subheader("📈 Time Series")

            if datetime_columns:

                date_column = st.selectbox(
                    "Date Column",
                    datetime_columns,
                    key="date_column"
                )

                value_column = st.selectbox(
                    "Numeric Value",
                    numeric_columns,
                    key="value_column"
                )

                line_chart = create_line_chart(
                    df,
                    date_column,
                    value_column
                )

                st.plotly_chart(
                    line_chart,
                    width="stretch",
                    key="line_chart"
                )

            else:

                st.info("No datetime columns detected.")
        with insights_tab:
            st.subheader("💡 AI Insights")
            st.info("Automatically generated insights and stories will appear here.")
            
    except Exception as e:
            st.error(f"Error loading dataset: {e}")