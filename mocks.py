"""Mocks for sensor and database client, for testing"""

# Mock database
def init_db(db_name, host='localhost', port=8086):
    """NOOP to initialize the database client"""
    return MockDBClient(db_name)

class MockDBClient:
    def __init__(self, db_name):
        self.db_name = db_name

    def write_points(self, sensor_data):
        """Print sensor data to stdout. Always returns True"""
        print(sensor_data)
        return True


# Mock sensor
def init_sensor(sensor_id, sensor_location):
    """Return a mock sensor object"""
    return MockSensor(sensor_id, sensor_location)

class MockSensor:
    sensor_type = "MockSensor"
    temperature = 21.12
    humidity = 51.50
    pressure = 1010.1010

    def __init__(self, sensor_id, sensor_location):
        self.sensor_id = sensor_id
        self.sensor_location = sensor_location

    def read_data(self):
        """NOOP: Read data from the sensor into our class variables"""
 