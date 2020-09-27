# bme280-logger
Read sensor data from a bme280 and upload to InfluxDB

Tested with Raspbian 10 (buster) on Raspberry Pi Zero W with
Adafruit BME280 hooked up over I2C. Should be reasonably easy
to adapt to different sensor types.


# Installation
1. Install InfluxDB and the python InfluxDB client:
    ```
    sudo apt-get install influxdb influxdb-client python3-influxdb
    ```
1. Install the BME280 and required libraries, and pytest:
    ```
    sudo pip3 install adafruit-circuitpython-bme280 pytest
    ```
1. Clone this repo someplace. 

1. Edit configuration in `sensor_config.py`

1. Edit `ExecStart` in `bme280-logger.service` to point
to the path to the logger service in the repo, then install and launch 
`bme280-logger.service`:
    ```
    sudo cp bme280-logger.service /etc/systemd/system
    sudo systemctl start bme280-logger.service
    sudo systemctl enable bme280-logger.service
    ```


# Testing
To test on a system without InfluxDB or a real BME280, use pytest:
```
python3 -m pytest bme280-logger.py
```
