FROM python:3.9.7-slim
RUN pip install pika
RUN pip install haversine
COPY station_worker /
COPY middleware/worker_middleware /middleware
COPY middleware/common_middleware /common_middleware
ENTRYPOINT ["/bin/sh"]