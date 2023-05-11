FROM python:3.9.7-slim
RUN pip install pika
COPY server /
COPY common /common_extra
ENTRYPOINT ["/bin/sh"]
