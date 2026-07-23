import pandas as pd


def load_dataset(uploaded_file):
    """
    Reads an uploaded CSV or Excel file and returns
    a Pandas DataFrame.

    Parameters
    ----------
    uploaded_file : UploadedFile
        File uploaded using Streamlit.

    Returns
    -------
    pandas.DataFrame
    """

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif file_name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format.")