FROM python:3.9.7-slim
RUN pip install pika
COPY weather_worker /
COPY worker_middleware /common_extra
ENTRYPOINT ["/bin/sh"]