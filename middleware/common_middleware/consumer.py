from common_middleware.communication import init_connection

class Consumer:
    def __init__(self, consumer_id, exchange, queue):
        self.exchange = exchange
        self.queue = queue
        self.consumer_id = consumer_id

    def add_keys(self, keys):
        _dict = {}
        for key in keys:
            _dict[key] = []
        return _dict

    def run(self):

        exchange = self.exchange
        exchange_list = []
        if exchange != '':
            exchange_list.append(exchange)
        connection, channel = init_connection(exchange_list)
        self.connection = connection

        result = channel.queue_declare(queue=self.queue)
        queue_name = result.method.queue

        if exchange != '':
            channel.queue_bind(exchange=exchange, queue=queue_name)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=lambda ch, method, properties, body: self.callback(ch, method, body))

        channel.start_consuming()

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass
