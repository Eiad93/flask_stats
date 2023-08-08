import uuid

import pandas as pd
from flask import request


def get_column_stats(df: pd.DataFrame, column_name: str):
    """
    Calculates the sum and mean of a specified column in the DataFrame for each Zeitindex.

    Additionally, it generates a plot for the calculated statistics, saving it in the 'plots/'
    folder under a uniquely generated ID as the filename. This generated ID is also included
    in the returned dictionary under the 'plot_id' key along with the calculated statistics.

    Args:
        df: The DataFrame containing the input CSV data.
        column_name: The column name for which statistic are to be generated.

    Returns:
        dict: containing column stats for each PID with the following structure
        {column_name: {PID_value: {'sum': sum_value, 'mean': mean_value}, ....}}.
    """
    if df[column_name].dtype == "object":
        try:
            # remove euro sign from string
            df[column_name] = df[column_name].str.replace("\x80", "")
            df[column_name] = df[column_name].astype(float)
        except ValueError as e:
            raise e
    groups = df.groupby("Zeitindex")[column_name].agg(["sum", "mean"])
    figure = groups.plot(kind="bar", title=f"{column_name} Sum and Mean").get_figure()
    figure_id = uuid.uuid4()
    figure.savefig(f"plots/{figure_id}.jpeg", bbox_inches="tight")
    return {
        "plot_uri": f"{request.root_url}plots/{figure_id}",
        column_name: groups.to_dict(orient="index"),
    }
