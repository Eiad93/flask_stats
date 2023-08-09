## Flask Stats

A simple flask app that generates basic statistics for a provided csv file.

## Endpoints
# Health Check
- Endpoint: /health/
- Method: GET
- Description: Returns "OK" with a status code of 200 if the app is operational.

# Generate Statistics from CSV
- Endpoint: /stats/
- Method: POST
- Description: Generates statistics for a specified column in a given CSV file.
- Parameters:
    - column: The target column for which statistics are to be generated.
    - sep: The CSV separator used in the provided CSV file.
- Request Body: The request body should contain the CSV file to analyze.

- Response:
    - 200 OK: Returns JSON response with statistics and plot ID.
    - 400 Bad Request: Returns an error message if the request is missing parameters or the CSV file.
    - 500 Internal Error: Returns an error message if the CSV file cannot be parsed.

# Retrieve Plot
- Endpoint: /plots/\<plot_id>
- Method: GET
- Description: Retrieves and returns an image (plot) from the 'plots/' directory via the Flask API.
- Parameters:
    - plot_id: The ID of the image to retrieve.
- Response:
    - 200 OK: Returns the requested image.
    - 404 Not Found: Returns an error message if the image is not found.
    - 500 Internal Error: Returns an error message if an internal error occurs.

## Running the App
- Running the app locally:
    - Install the required dependencies by running pip install -r requirements.txt.
    - Run the Flask app by executing `flask --app main run --host 0.0.0.0 --port=8080`.
    - The app will be accessible at http://localhost:8080.
- Running the app with Docker:
    - Run `docker build -t <image-tag> .`
    - Run `docker run -p 8080:8080 --name <container-name> <image-tag>`

## Usage
- Use the /health/ endpoint to check if the app is operational.

    ```
        curl -X GET http://localhost:8080/health/
    ```
- To generate statistics from a CSV file:
    - Make a POST request to the /stats/ endpoint.
    - Include the column and sep parameters in the query string.
    - Attach the CSV file to the request body.
    - Make sure to add the header `-H 'Content-Type: application/json'` when making requests for the stats endpoint.

    ```
    curl -X POST --data-binary "@test.csv" -H 'Content-Type: application/json' http://localhost:8080/stats/\?column\=$column\&sep\=$separator
    ```
- To retrieve a plot:
    - Make a GET request to the /plots/<plot_id> endpoint, where <plot_id> is the desired plot's ID.

    ```
    curl -X GET http://localhost:8080/plots/<plot_id> > <file_name.png>
    ```
    This will save the image to the local disk under the choses file name.
