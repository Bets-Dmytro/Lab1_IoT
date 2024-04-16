from csv import reader

from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.gps_filename = gps_filename
        self.f_gps = None
        self.gps = None
        self.gps_counter = 0

        self.accelerometer_filename = accelerometer_filename
        self.f_acc = None
        self.accelerometer = None
        self.accelerometer_counter = 0

        self.parking_filename = parking_filename
        self.f_prk = None
        self.parking = None
        self.parking_counter = 0

        self.stop_read = False

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        data_gps = self.gps[self.gps_counter]
        longitude, latitude = float(data_gps[0]), float(data_gps[1])
        self.gps_counter = (self.gps_counter + 1) % len(self.gps)

        data_accelerometer = self.accelerometer[self.accelerometer_counter]
        x, y, z = int(data_accelerometer[0]), int(data_accelerometer[1]), int(data_accelerometer[1])
        self.accelerometer_counter = (self.accelerometer_counter + 1) % len(self.accelerometer)

        data_parking = self.parking[self.parking_counter]
        empy_count, longitude_p, latitude_p = int(data_parking[0]), float(data_parking[1]), float(data_parking[2])
        self.parking_counter = (self.parking_counter + 1) % len(self.parking)

        return AggregatedData(
            Accelerometer(x, y, z),
            Gps(longitude, latitude),
            Parking(empy_count, Gps(longitude_p, latitude_p)),
            datetime.now()
        )

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.f_gps = open(self.gps_filename)
        data_csv = reader(self.f_gps)
        next(data_csv)
        self.gps = list(data_csv)

        self.f_acc = open(self.accelerometer_filename)
        data_csv = reader(self.f_acc)
        next(data_csv)
        self.accelerometer = list(data_csv)

        self.f_prk = open(self.parking_filename)
        data_csv = reader(self.f_prk)
        next(data_csv)
        self.parking = list(data_csv)

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.f_gps.close()
        self.f_acc.close()
        self.f_prk.close()
