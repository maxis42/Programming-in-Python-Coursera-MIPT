class Value:
    def __init__(self):
        self.value = None

    @staticmethod
    def _remove_comission(obj, value):
        attr_name = "commission"
        assert hasattr(obj, attr_name), \
            f"{obj} doesn't have attribute \"{attr_name}\""

        res = value * (1 - obj.commission)
        return res

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, value):
        self.value = self._remove_comission(obj, value)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == "__main__":
    new_acc = Account(0.1)
    new_acc.amount = 100

    print(new_acc.amount)
