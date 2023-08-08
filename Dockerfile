FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
