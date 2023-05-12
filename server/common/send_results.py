from middleware.protocol import send_string
import json
import common.config as config

def send_results(skt, result, error):
    if error == config.ERROR_MESSAGE:
        send_string(skt, config.ERROR_MESSAGE)
        return
    result_string = json.dumps(result)
    send_string(skt, result_string)