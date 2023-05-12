from common_middleware.communication import init_connection, publish_message

def send_message(message, queue):
    connection, channel = init_connection([])

    channel.queue_declare(queue=queue)

    publish_message(channel, '', queue, message)
    connection.close()




   