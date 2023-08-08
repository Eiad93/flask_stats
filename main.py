import io
import os
import logging

from flask import Flask, request, jsonify, send_from_directory
import pandas as pd

from .utils.validate_df import all_required_columns_exist
from .utils.generate_stats import get_column_stats

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/health/", methods=["GET"])
def health_check():
    """Returns 'OK' if a GET request is sucessfully made."""
    return "OK", 200


@app.route("/stats/", methods=["POST"])
def generate_stats_from_csv():
    """
    Generate statistics for a specified column in a given CSV file.

    This endpoint accepts a CSV file upload along with 'column' and 'sep'
    parameters. 'column' denotes the target column for which statistics are
    to be generated, and 'sep' indicates the CSV separator used in the
    provided CSV file.

    Returns:
        JSON response with statistics and plot ID or an error message.

    Raises:
        HTTP 400 Bad Request:
            - If the csv file or any of the parameters is missing.
            - If any of the columns PID, Zeitindex or the specified
              column does not exist in the csv file.
        HTTP 500 Internal Error:
            - If the CSV file cannot be Parsed.
    """
    csv_data = request.data

    if not csv_data:
        return jsonify({"error": "No CSV file was provided"}), 400

    column_name = request.args.get("column")
    column_sep = request.args.get("sep")

    if not column_name or not column_sep:
        return (
            jsonify({"error": "Request is missing the column or sep parameter"}),
            400,
        )

    logger.info(
        f"Successfuly received a POST request with the following input parameters. "
        f"column name {column_name}, separator {column_sep}, CSV file size {len(csv_data)} bytes."
    )

    try:
        input_df = pd.read_csv(io.BytesIO(csv_data), sep=column_sep, encoding="latin1")
    except Exception as e:
        logger.info(f"Error while attempting to parse the CSV file. {str(e)}")
        return jsonify({"error": "An internal error has occurred"}), 500

    logger.info("Successfully parsed CSV file.")

    if not all_required_columns_exist(input_df, column_name):
        return (
            jsonify(
                {
                    "error": f"One of the required columns (PID, Zeitindex, {column_name}) "
                    f"is missing or the choosen separator '{column_sep}' is not correct."
                }
            ),
            400,
        )

    try:
        stats = get_column_stats(input_df, column_name)
    except ValueError:
        return (
            jsonify(
                {
                    "error": "The selected column needs to be of numerical or boolean type"
                }
            ),
            400,
        )

    logger.info("Sucessfuly generated column statistics.")

    return jsonify(stats), 200


@app.route("/plots/<string:plot_id>", methods=["GET"])
def get_plot(plot_id: str):
    """Retrieve and return an image from the 'plots/' directory via the Flask API.

    Args:
        plot_id: The ID of the image to retrieve.

    Returns:
        flask.Response: A Flask Response object containing the requested image.
    """
    try:
        plot_filename = f"{plot_id}.jpeg"
        plot_path = f"plots/{plot_filename}"
        if os.path.exists(plot_path):
            return send_from_directory("plots/", plot_filename)
        else:
            return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching the plot with ID {plot_id}. {str(e)}")
        return jsonify({"error": "An internal error has occurred"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
