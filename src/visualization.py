import plotly.express as px
import pandas as pd


def create_histogram(df: pd.DataFrame, column: str):
    """
    Create a histogram for a numeric column.
    """

    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=f"Distribution of {column}"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig
def create_boxplot(df: pd.DataFrame, column: str):
    """
    Create a box plot for a numeric column.
    """

    fig = px.box(
        df,
        y=column,
        title=f"Box Plot of {column}",
        points="outliers"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig

def create_correlation_heatmap(df: pd.DataFrame):
    """
    Create a correlation heatmap for numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    correlation_matrix = numeric_df.corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Correlation Heatmap"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig

def create_scatter_plot(df: pd.DataFrame, x_column: str, y_column: str):
    """
    Create a scatter plot between two numeric columns.
    """

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} vs {x_column}",
        opacity=0.7,
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig

def create_bar_chart(df: pd.DataFrame, column: str):
    """
    Create a bar chart for a categorical column.
    """

    counts = (
        df[column]
        .value_counts()
        .head(10)
        .reset_index()
    )

    counts.columns = [column, "Count"]

    fig = px.bar(
        counts,
        x=column,
        y="Count",
        title=f"Distribution of {column}"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig

def create_line_chart(df: pd.DataFrame, date_column: str, value_column: str):
    """
    Create a line chart using a datetime column and a numeric column.
    """

    temp_df = df.copy()

    temp_df[date_column] = pd.to_datetime(
        temp_df[date_column],
        errors="coerce"
    )

    temp_df = temp_df.dropna(subset=[date_column])

    temp_df = (
        temp_df
        .sort_values(date_column)
        .groupby(date_column)[value_column]
        .sum()
        .reset_index()
    )

    fig = px.line(
        temp_df,
        x=date_column,
        y=value_column,
        title=f"{value_column} Over Time"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def detect_datetime_columns(df: pd.DataFrame):
    """
    Detect datetime columns, including those stored as strings.
    """

    datetime_columns = []

    for column in df.columns:


        if pd.api.types.is_datetime64_any_dtype(df[column]):
            datetime_columns.append(column)
            continue

        if not (
            pd.api.types.is_object_dtype(df[column])
            or pd.api.types.is_string_dtype(df[column])
        ):
            continue

        series = df[column].dropna()

        if series.empty:
            continue

        try:
            parsed = pd.to_datetime(
                series,
                errors="coerce",
                format="mixed"
            )

            success_rate = parsed.notna().mean()

            if success_rate >= 0.8:
                datetime_columns.append(column)

        except Exception:
            continue

    return datetime_columns