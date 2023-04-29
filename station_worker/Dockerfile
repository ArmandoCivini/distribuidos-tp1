FROM python:3.9.7-slim
RUN pip install pika
RUN pip install haversine
COPY station_worker /
COPY common /common_extra
ENTRYPOINT ["/bin/sh"]