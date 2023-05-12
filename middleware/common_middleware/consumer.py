import pika

class Consumer:
    def __init__(self, consumer_id, exchange, queue):
        self.exchange = exchange
        self.queue = queue
        self.consumer_id = consumer_id
        #TODO: add del func

    def add_keys(self, keys):
        _dict = {}
        for key in keys:
            _dict[key] = []
        return _dict

    def run(self):

        exchange = self.exchange
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        if exchange != '':
            channel.exchange_declare(exchange=exchange, exchange_type='fanout')

        result = channel.queue_declare(queue=self.queue)
        queue_name = result.method.queue

        if exchange != '':
            channel.queue_bind(exchange=exchange, queue=queue_name)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=lambda ch, method, properties, body: self.callback(ch, method, body))

        channel.start_consuming()
