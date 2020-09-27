"""Encapsulation and utilities for the Adafruit BME280 sensor library"""

import board
import digitalio
import busio
import adafruit_bme280

def init_sensor(sensor_id, sensor_location):
    """Return a new sensor"""
    sensor = BME280Sensor(sensor_id, sensor_location)
    return sensor

class BME280Sensor:
    """Encapsulates Adafruit BME280 library"""
    sensor_type = "BME280"
    temperature = None
    humidity = None
    pressure = None 

    def __init__(self, sensor_id, sensor_location):
        self.sensor_id = sensor_id
        self.sensor_location = sensor_location
        # Create library object using our Bus I2C port
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    def read_data(self):
        """Read data from the sensor into our class variables"""
        self.temperature = self.bme280.temperature
        self.humidity = self.bme280.humidity
        self.pressure = self.bme280.pressure
