from tempfile import gettempdir
import os


class File:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

    def __add__(self, other):
        assert isinstance(other, File)

        temp_dir = gettempdir()
        temp_path = os.path.join(temp_dir, "temp.txt")

        new_obj = File(temp_path)
        new_obj.write(self.read(), "w")
        new_obj.write(other.read(), "a")
        return new_obj

    def read(self):
        with open(self.path, "r") as f:
            data = f.read()

        return data

    def write(self, s, mode="w"):
        if mode not in {"w", "a"}:
            raise ValueError

        with open(self.path, mode) as f:
            f.write(s)

    def __iter__(self):
        self.cur_byte = 0
        self.num_bytes = os.path.getsize(self.path)
        return self

    def __next__(self):
        if self.cur_byte >= self.num_bytes:
            raise StopIteration("EOF")

        with open(self.path, "r") as f:
            f.seek(self.cur_byte)
            row = f.readline()
            self.cur_byte = f.tell()
        return row
