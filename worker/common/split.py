import pika
import logging

def callback(ch, method, properties, body):
    if body.decode("utf-8")  == 'end':
        logging.info('received end for trips')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
        return
    logging.info("Received trip {}".format(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)



def split():
    trips_queue = 'trips_queue'#TODO: add to configuration
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue=trips_queue, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=trips_queue, on_message_callback=callback)
    logging.info(f"starting consuming trips")
    channel.start_consuming()
    logging.info(f"finished consuming trips")