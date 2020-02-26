import socket
import time
import re


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout  # seconds
        self.sock = self._sock

    @property
    def _sock(self):
        socket.setdefaulttimeout(self.timeout)
        # sock = socket.socket()
        # sock.connect((self.host, self.port))
        sock = socket.create_connection((self.host, self.port), self.timeout)
        # sock.settimeout(self.timeout)
        # sock.listen(1)
        # sock.listen(socket.SOMAXCONN)
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

        query = " ".join(["put", str(metric_type), str(metric_value),
                          str(timestamp)])
        query += "\n"

        self.sock.sendall(query.encode("utf-8"))
        status, data = self._get_response()

        if status == "error":
            raise ClientError()

    def __del__(self):
        self.sock.close()

    def _get_response(self):
        data = self.recvall(self.sock)
        response = data.decode("utf-8")
        self._check_response(response)
        response_data = response.split()
        status = response_data[0]
        data = response_data[1:]
        return status, data

    @staticmethod
    def _check_response(s):
        data = s.split("\n")
        status = data[0]
        if status not in {"ok", "error"}:
            raise ClientError()

        if (data[-1] != "") or (data[-2] != ""):
            raise ClientError()

        content = data[1:-2]

        if (status == "error") and (content != "wrong command"):
            raise ClientError()

        for metric in content:
            metric_data = metric.split(" ")
            if len(metric_data) != 3:
                raise ClientError()

            metric_type, metric_value, timestamp = metric_data

            if re.fullmatch("\w+\.\w+", metric_type) is None:
                raise ClientError()

            if re.fullmatch("[-+]?\d*\.\d+|\d+", metric_value) is None:
                raise ClientError()

            if re.fullmatch("\d+", timestamp) is None:
                raise ClientError()

    # @staticmethod
    # def fullmatch(regex, string, flags=0):
    # PYTHON 2
    #     """Emulate python-3.4 re.fullmatch()."""
    #     return re.match("(?:" + regex + r")\Z", string, flags=flags)

    @staticmethod
    def recvall(sock):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

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


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=5)

    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)

    print(client.get("*"))
