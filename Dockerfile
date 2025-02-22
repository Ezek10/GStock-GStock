FROM python:3.11.4

WORKDIR /code

RUN apt-get update && apt-get install -y postgresql-client

COPY ./secret.json /code/secret.json

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/ /code/src

CMD ["uvicorn", "src.main.app:app", "--host", "0.0.0.0", "--port", "80"]
