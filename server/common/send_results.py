from common.protocol import send_string
import json

def send_results(skt, result, error):
    if error == 'error':
        send_string(skt, "error")
        return
    result_string = json.dumps(result)
    send_string(skt, result_string)