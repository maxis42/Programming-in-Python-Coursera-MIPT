import asyncio
import re


class Server(asyncio.Protocol):
    resp_ok = "ok\n\n"
    resp_err = "error\nwrong command\n\n"
    metrics = dict()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        msg = data.decode()
        status, cmd, data = self._parse_query(msg)

        if status == "error":
            response = Server.resp_err
        else:
            response = Server.resp_ok
            if cmd == "get":
                response = self.get_metrics(data)
            elif cmd == "put":
                response = self.put_metrics(data)

        print("response", response)
        self.transport.write(response.encode())

    @staticmethod
    def _parse_query(query):
        try:
            status = "ok"
            cmd, data = query.split(" ", 1)
            data = data.strip()

            if cmd == "get":
                if (data != "*") and (re.fullmatch("\S+", data) is None):
                    raise
            elif cmd == "put":
                metric_type, metric_value, timestamp = data.split(" ", 3)

                if re.fullmatch("\S+", metric_type) is None:
                    raise

                if re.fullmatch("[-+]?\d*\.\d+|\d+", metric_value) is None:
                    raise

                if re.fullmatch("\d+", timestamp) is None:
                    raise
            else:
                raise
        except:
            status = "error"
            cmd = None
            data = None

        return status, cmd, data

    def send_client_error(self):
        self.transport.write(Server.resp_err.encode())

    def get_metrics(self, data):
        response = Server.resp_ok

        if data == "*":
            response = "ok\n"

            for metric_type, metric_data in self.metrics.items():
                for timestamp, metric_value in metric_data:
                    response += f"{metric_type} {metric_value} {timestamp}\n"

            response += "\n"
        else:
            metric_type = data

            if metric_type not in self.metrics:
                response = Server.resp_ok
            else:
                response = "ok\n"

                for timestamp, metric_value in self.metrics[metric_type]:
                    response += f"{metric_type} {metric_value} {timestamp}\n"

                response += "\n"

        return response

    def put_metrics(self, data):
        data_split = data.split(" ", 3)

        metric_type, metric_value, timestamp = data_split

        metric_value = float(metric_value)
        timestamp = int(timestamp)

        if metric_type not in self.metrics:
            self.metrics[metric_type] = []

        self.metrics[metric_type] = list(filter(lambda x: x[0] != timestamp,
                                                self.metrics[metric_type]))

        self.metrics[metric_type].append((timestamp, metric_value))

        for metric_type in self.metrics:
            self.metrics[metric_type] = sorted(self.metrics[metric_type],
                                               key=lambda x: x[0])

        response = "ok\n\n"
        return response


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 10010)
