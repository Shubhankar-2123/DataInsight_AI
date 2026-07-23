import pandas as pd


def generate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate descriptive statistics for all numeric columns.

    Returns
    -------
    pandas.DataFrame
        Statistics for numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    statistics = pd.DataFrame({
        "Count": numeric_df.count(),
        "Mean": numeric_df.mean(),
        "Median": numeric_df.median(),
        "Mode": numeric_df.mode().iloc[0],
        "Minimum": numeric_df.min(),
        "Maximum": numeric_df.max(),
        "Std Dev": numeric_df.std(),
    })

    return statistics.round(2)