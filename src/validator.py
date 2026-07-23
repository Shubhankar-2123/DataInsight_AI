import pandas as pd


def validate_dataset(df: pd.DataFrame):
    """
    Validate the uploaded dataset.

    Returns:
        (bool, str)
    """

    if df.empty:
        return False, "The uploaded dataset is empty."

    if df.shape[0] == 0:
        return False, "The dataset contains no rows."

    if df.shape[1] == 0:
        return False, "The dataset contains no columns."

    return True, "Dataset is valid."