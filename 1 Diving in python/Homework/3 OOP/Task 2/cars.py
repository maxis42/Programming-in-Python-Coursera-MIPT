import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        """
        Get photo file extension ('.png', '.jpeg', etc).
        :return: str, file extension
        """
        file_ext = os.path.splitext(self.photo_file_name)[1]
        return file_ext

    @property
    def car_type(self):
        raise NotImplementedError


class Car(CarBase):
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self.body_length, self.body_width, self.body_height = self.get_body_whl()

    def get_body_whl(self):
        """
        Get body length, width, height
        :return: tuple of floats, length, width, height
        """
        if self.body_whl:
            length, width, height = list(map(float, self.body_whl.split("x")))
        else:
            length = width = height = 0.0
        return length, width, height

    def get_body_volume(self):
        """
        Get body volume
        :return: float, body volume
        """
        body_volume = self.body_length * self.body_width * self.body_height
        return body_volume


class SpecMachine(CarBase):
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_f):
    car_list = []

    with open(csv_f) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) < 7:
                continue

            type = row[0]
            brand = row[1]
            if row[2]:
                passenger_seats_cnt = int(row[2])
            photo_f = row[3]
            if row[4]:
                body_whl = row[4]
            carrying = float(row[5])
            if row[6]:
                extra = row[6]

            if type == "car":
                car = Car(brand, photo_f, carrying, passenger_seats_cnt)
            elif type == "truck":
                car = Truck(brand, photo_f, carrying, body_whl)
            elif type == "spec_machine":
                car = SpecMachine(brand, photo_f, carrying, extra)
            else:
                raise ValueError(f"Unknown car type: {type}")

            car_list.append(car)

    return car_list


if __name__ == '__main__':
    csv_filename = "coursera_week3_cars.csv"

    cars = get_car_list(csv_filename)
