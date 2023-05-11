FROM python:3.9.7-slim
RUN pip install pika
COPY weather_worker /
COPY middleware/worker_middleware /middleware
ENTRYPOINT ["/bin/sh"]