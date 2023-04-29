FROM python:3.9.7-slim
RUN pip install pika
RUN pip install haversine
COPY station_worker /
ENTRYPOINT ["/bin/sh"]