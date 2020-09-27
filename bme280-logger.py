import time
import math
import sys
import sensor_config

# Lightweight way to test with mocks in environments where
# the adafruit and/or influxdb libs are not installed
if "pytest" in sys.modules:
    from mocks import init_db, init_sensor
else:
    from influxdb_wrapper import init_db
    from bme280 import init_sensor

# For testing
import pytest
import json

def ctof(temp_c):
    """Convert temperature from celsius to fahrenheit"""
    return temp_c * (9/5) + 32

@pytest.mark.parametrize("input, expected", [(0,32), (100,212), (21,69.8), (-12,10.4)])
def test_ctof(input, expected):
    assert ctof(input) == pytest.approx(expected)


# B+C are constants for calculating dew point
B = 17.62
C = 243.12
def calc_dewpoint(temp, humidity):
    """Calculate the dew point using Magnus formula w/ Sonntag constants"""
    gamma = (B * temp /(C + temp)) + math.log(humidity / 100.0)
    return (C * gamma) / (B - gamma)

@pytest.mark.parametrize("input_t, input_h, expected", [(21,65,14.1664), (0,70,-4.82374), (90,100,90)])
def test_calc_dewpoint(input_t, input_h, expected):
    assert calc_dewpoint(input_t, input_h) == pytest.approx(expected)


def print_data(temperature, humidity, pressure, dewpoint):
    print("Temperature: %0.1f C, %0.1f F" % (temperature, ctof(temperature)))
    print("Humidity: %0.1f %%" % humidity)
    print("Pressure: %0.1f hPa" % pressure)
    print("Dewpoint: %0.1f C, %0.1f F" % (dewpoint, ctof(dewpoint)))

def read_sensor_data(sensor):
    """Read data from the sensor and send it to the database"""
    sensor.read_data()
    temperature = sensor.temperature
    humidity = sensor.humidity
    pressure = sensor.pressure
    dewpoint = calc_dewpoint(temperature, humidity) 

    sensor_data = [
        {
            "measurement": sensor_config.MEASUREMENT_NAME,
            "tags": {
                "sensor_ID":       sensor.sensor_id,
                "sensor_type":     sensor.sensor_type,
                "sensor_location": sensor.sensor_location,
            },
            "fields": {
                "temp_c":       temperature,
                "temp_f":       ctof(temperature),
                "rel_humidity": humidity,
                "pressure_hPa": pressure,
                "dewpoint_c":   dewpoint,
                "dewpoint_f":   ctof(dewpoint),
            }
        }
    ]
    return sensor_data

def test_read_sensor_data():
    sensor = init_sensor(sensor_config.SENSOR_ID, sensor_config.SENSOR_LOCATION)
    sensor_data = read_sensor_data(sensor)
    assert json.dumps(sensor_data) == (
        '[{"measurement": "sensor_reading", '
        '"tags": {"sensor_ID": "0001", '
        '"sensor_type": "MockSensor", '
        '"sensor_location": "dining room"}, '
        '"fields": {"temp_c": 21.12, '
        '"temp_f": 70.016, '
        '"rel_humidity": 51.5, '
        '"pressure_hPa": 1010.101, '
        '"dewpoint_c": 10.72925621235596, '
        '"dewpoint_f": 51.31266118224073}}]'
    )


def main():
    sensor = init_sensor(sensor_config.SENSOR_ID, sensor_config.SENSOR_LOCATION)
    db_client = init_db('sensors')
    while True:
        timestamp = time.time()
        print("Reading sensor at: ", time.strftime('%a %Y-%m-%d %H:%M:%S %p %Z', time.localtime(timestamp)))
        sensor_data = read_sensor_data(sensor)
        if not db_client.write_points(sensor_data):
            print("Error writing data to DB!")
            break
        time.sleep(sensor_config.DELAY)

if __name__ == '__main__':
    main()
