FROM python:3.9.7-slim
RUN pip install pika
COPY worker.py /root/worker.py
CMD /root/worker.py