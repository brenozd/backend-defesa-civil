# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /backend/

ENV MONGO_HOST "mongo-db"
ENV MQTT_HOST "mqtt"

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && rm requirements.txt

ADD src/ /backend/
RUN chmod +x /backend/app.py

CMD ["sh", "-c", "./app.py --mongo ${MONGO_HOST} --mqtt ${MQTT_HOST}"]