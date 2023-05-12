FROM python:3.9.7-slim
RUN pip install pika
COPY result_reducer /
COPY middleware/common_middleware /common_middleware
ENTRYPOINT ["/bin/sh"]
