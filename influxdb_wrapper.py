"""Wrapper for InfluxDBClient"""

from influxdb import InfluxDBClient

def init_db(db_name, host='localhost', port=8086):
    client = InfluxDBClient(host, port)
    client.switch_database(db_name)
    return client
