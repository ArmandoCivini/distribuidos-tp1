FROM python:3.9.7-slim
RUN pip install pika
COPY server /
COPY middleware/endpoint_middleware /middleware
COPY middleware/common_middleware /common_middleware
ENTRYPOINT ["/bin/sh"]
