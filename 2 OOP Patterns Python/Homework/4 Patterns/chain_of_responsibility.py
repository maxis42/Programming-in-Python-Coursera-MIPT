class SomeObject:
    def __init__(self, integer_field=0, float_field=0.0, string_field=""):
        self.integer_field = integer_field
        self.float_field = float_field
        self.string_field = string_field


class EventGet:
    """
    EventGet(<type>) создаёт событие получения данных соответствующего типа
    """
    def __init__(self, type_):
        self.type_s = None
        if type_ is int:
            self.type_s = "int"
        elif type_ is float:
            self.type_s = "float"
        elif type_ is str:
            self.type_s = "str"
        else:
            raise NotImplementedError()


class EventSet:
    """
    EventSet(<value>) создаёт событие изменения поля типа type(<value>)
    """
    def __init__(self, value):
        self.value = value

        self.type_s = None

        if isinstance(self.value, int):
            self.type_s = "int"
        elif isinstance(self.value, float):
            self.type_s = "float"
        elif isinstance(self.value, str):
            self.type_s = "str"
        else:
            raise NotImplementedError()


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.type_s == "int":
            if isinstance(event, EventGet):
                return obj.integer_field
            elif isinstance(event, EventSet):
                obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.type_s == "float":
            if isinstance(event, EventGet):
                return obj.float_field
            elif isinstance(event, EventSet):
                obj.float_field = event.value
        else:
            print("float")
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.type_s == "str":
            if isinstance(event, EventGet):
                return obj.string_field
            elif isinstance(event, EventSet):
                obj.string_field = event.value
        else:
            return super().handle(obj, event)


if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"

    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))

    print(chain.handle(obj, EventGet(int)))
    print(chain.handle(obj, EventGet(float)))
    print(chain.handle(obj, EventGet(str)))

    print(chain.handle(obj, EventSet(100)))
    print(chain.handle(obj, EventGet(int)))

    print(chain.handle(obj, EventSet(0.5)))
    print(chain.handle(obj, EventGet(float)))

    print(chain.handle(obj, EventSet("new text")))
    print(chain.handle(obj, EventGet(str)))

    obj = SomeObject(integer_field=76, float_field=15.7546, string_field="OxMYqF")
    print(chain.handle(obj, EventGet(int)))

    obj = SomeObject(integer_field=33, float_field=-15.0501, string_field="jSxvNm")
    print(chain.handle(obj, EventGet(float)))
