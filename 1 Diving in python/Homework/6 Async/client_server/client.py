import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout  # seconds
        self.sock = self._sock

    @property
    def _sock(self):
        socket.setdefaulttimeout(self.timeout)
        sock = socket.create_connection((self.host, self.port), self.timeout)
        sock.settimeout(self.timeout)
        return sock

    def get(self, metric_type):
        query = " ".join(["get", metric_type])
        query += "\n"

        self.sock.sendall(query.encode("utf-8"))
        status, data = self._get_response()

        if status == "error":
            raise ClientError()

        metrics_data = self._parse_get_data(data)
        return metrics_data

    def put(self, metric_type, metric_value, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        query = " ".join(["put", metric_type, metric_value, timestamp])
        query += "\n"

        self.sock.sendall(query.encode("utf-8"))
        status, data = self._get_response()

        if status == "error":
            raise ClientError()

    def __del__(self):
        self.sock.close()

    def _get_response(self):
        response = ""
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            response += data.decode("utf-8")

        response_data = response.split()
        status = response_data[0]
        data = response_data[1:]
        return status, data

    @staticmethod
    def _parse_get_data(data):
        data = iter(data)
        data = zip(data, data, data)

        metrics_data = {}
        for metric_type, metric_value, timestamp in data:
            metric_value = float(metric_value)
            timestamp = int(timestamp)

            if metric_type not in metrics_data:
                metrics_data[metric_type] = []

            metrics_data[metric_type].append((timestamp, metric_value))

        for metric_type in metrics_data:
            metrics_data[metric_type] = sorted(metrics_data[metric_type],
                                               key=lambda x: x[0])
        return metrics_data


class ClientError(Exception):
    pass
