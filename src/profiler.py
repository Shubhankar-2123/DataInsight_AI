import pandas as pd


def get_dataset_overview(df: pd.DataFrame):
    """
    Generate a high-level overview of the dataset.

    Returns:
        dict: Dataset overview information.
    """

    overview = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "numeric_columns": len(df.select_dtypes(include="number").columns),
        "categorical_columns": len(df.select_dtypes(include="object").columns),
        "datetime_columns": len(df.select_dtypes(include="datetime").columns),
        "memory_usage": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
    }

    return overview