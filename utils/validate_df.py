import pandas as pd


def all_required_columns_exist(df: pd.DataFrame, column_name: str):
    """
    Checks if the DataFrame contains all required column for stats generation.

    It specificly checks if columns PID, Zeitindex and the selected column
    given by the column_name are available in the df.

    Args:
        df: The DataFrame containing the input CSV data.
        column_name: The column name for which statistic are to be generated.

    Returns:
        bool: True if all required columns exist, else False.
    """
    required_columns = ["PID", "Zeitindex", column_name]
    return all(column in df.columns for column in required_columns)
