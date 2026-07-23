import pandas as pd


def analyze_data_quality(df: pd.DataFrame):
    """
    Analyze the quality of the dataset.

    Returns:
        dict
    """

    missing_values = df.isnull().sum()

    duplicate_rows = df.duplicated().sum()

    empty_columns = df.columns[df.isnull().all()].tolist()

    constant_columns = [
        column
        for column in df.columns
        if df[column].nunique(dropna=False) == 1
    ]

    return {
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "empty_columns": empty_columns,
        "constant_columns": constant_columns,
    }