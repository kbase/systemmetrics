import socket
import json
import os

host = os.environ.get("ELASTICSEARCH_HOST")
if host is None:
    print("No value set for ELASTICSEARCH_HOST environment variable, output will be send to stdout")


def to_logstashJson(log_d):

    port = 9000
    json_data = json.dumps(log_d)
    json_data += '\n'

    if host is not None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(json_data.encode())
    else:
        print(json_data)

    return None
