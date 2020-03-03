"""
Это вспомогательный скрипт для тестирования сервера из задания на неделе 6.

Для запуска скрипта на локальном компьютере разместите рядом файл client.py,
где содержится код клиента, который открывается по прохождении задания
недели 5.

Сначала запускаете ваш сервер на адресе 127.0.0.1 и порту 8888, а затем
запускаете этот скрипт.
"""
import sys
from client_solution import Client, ClientError


def run(host, port):
    client1 = Client(host, port, timeout=5)
    client2 = Client(host, port, timeout=5)
    command = "wrong command test\n"
    # self._send(f"get {key}\n".encode())

    try:
        data = client1.get(command)
        print(data.decode())
    except ClientError:
        pass
    except BaseException as err:
        print(f"Ошибка соединения с сервером: {err.__class__}: {err}")
        sys.exit(1)
    else:
        print("Неверная команда, отправленная серверу, должна возвращать "
              "ошибку протокола")
        sys.exit(1)

    command = 'some_key'
    # command = "\n"
    data_1 = data_2 = ""
    try:
        data_1 = client1.get(command)
        data_2 = client1.get(command)
    except ClientError:
        print(
            'Сервер вернул ответ на валидный запрос, который клиент '
            'определил, как не корректный.. '
        )
    except BaseException as err:
        print(
            f"Сервер должен поддерживать соединение с клиентом между "
            f"запросами, повторный запрос к серверу завершился ошибкой: "
            f"{err.__class__}: {err}"
        )
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "На запрос клиента на получения данных по не существующему ключу, " \
        "сервер вдолжен озвращать ответ с пустым полем данных."

    try:
        data_1 = client1.get(command)
        data_2 = client2.get(command)
    except ClientError:
        print('Сервер вернул ответ на валидный запрос, который клиент '
              'определил, как не корректный.. ')
    except BaseException as err:
        print(f"Сервер должен поддерживать соединение с несколькими "
              f"клиентами: {err.__class__}: {err}")
        sys.exit(1)

    assert data_1 == data_2 == {}, \
        "На запрос клиента на получения данных по не существующему ключу, " \
        "сервер должен возвращать ответ с пустым полем данных."

    try:
        client1.put("k1", 0.25, timestamp=1)
        # client1.put("\n", "", "")
        client2.put("k1", 2.156, timestamp=2)
        client1.put("k1", 0.35, timestamp=3)
        client2.put("k2", 30, timestamp=4)
        client1.put("k2", 40, timestamp=5)
        client1.put("k2", 41, timestamp=5)
    except Exception as err:
        print(f"Ошибка вызова client.put(...) {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {
        "k1": [(1, 0.25), (2, 2.156), (3, 0.35)],
        "k2": [(4, 30.0), (5, 41.0)],
    }

    try:
        metrics = client1.get("*")
        if metrics != expected_metrics:
            print(f"client.get('*') вернул неверный результат. Ожидается: "
                  f"{expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('*') {err.__class__}: {err}")
        sys.exit(1)

    expected_metrics = {"k2": [(4, 30.0), (5, 41.0)]}

    try:
        metrics = client2.get("k2")
        if metrics != expected_metrics:
            print(f"client.get('k2') вернул неверный результат. Ожидается: "
                  f"{expected_metrics}. Получено: {metrics}")
            sys.exit(1)
    except Exception as err:
        print(f"Ошибка вызова client.get('k2') {err.__class__}: {err}")
        sys.exit(1)

    try:
        result = client1.get("k3")
        if result != {}:
            print(
                f"Ошибка вызова метода get с ключом, который еще не был "
                f"добавлен. "
                f"Ожидается: пустой словарь. Получено: {result}"
            )
            sys.exit(1)
    except Exception as err:
        print(
            f"Ошибка вызова метода get с ключом, который еще не был добавлен: "
            f"{err.__class__} {err}"
        )
        sys.exit(1)

    print("Похоже, что все верно! Попробуйте отправить решение на проверку.")


if __name__ == "__main__":
    run("127.0.0.1", 10010)
