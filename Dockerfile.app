FROM python:3.12-alpine

WORKDIR /code

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=docker
RUN apk update
RUN apk add --no-cache build-base gcc musl-dev linux-headers postgresql-libs postgresql-dev postgresql-client
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT ["./entrypoint.sh"]
