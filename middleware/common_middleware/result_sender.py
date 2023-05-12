import json
from common_middleware.message_sender import send_message

def send_results(results, queue):
    send_message(json.dumps(results), queue)




   