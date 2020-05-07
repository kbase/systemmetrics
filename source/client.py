import socket
import json
import os
host = os.environ["ELASTICSEARCH_HOST"]
def to_logstashJson(log_d):

    port = 9000
    json_data = json.dumps(log_d)
    json_data += '\n'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(json_data.encode())

    return None
