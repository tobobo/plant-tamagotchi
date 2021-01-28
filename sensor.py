import asyncio
import logging
import os
import sys
import math
from datetime import datetime
from lib.moisture_sensor import GroveMoistureSensor

INTERVAL = 5

NUM_MEAN_MOISTURE_SAMPLES = 10

BASE_THRESHOLDS = {
    'very-dry': 1550,
    'dry': 1500,
    'moist': 1410,
}

BUFFER = 5

MOISTURE_THRESHOLDS = {
    None: [
        ('very-dry', BASE_THRESHOLDS['very-dry']),
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf),
    ],
    'very-dry': [
        ('very-dry', BASE_THRESHOLDS['very-dry'] - BUFFER),
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf)
    ],
    'dry': [
        ('very-dry', BASE_THRESHOLDS['very-dry'] + BUFFER),
        ('dry', BASE_THRESHOLDS['dry'] - BUFFER),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf)
    ],
    'moist': [
        ('very-dry', BASE_THRESHOLDS['very-dry']),
        ('dry', BASE_THRESHOLDS['dry'] + BUFFER),
        ('moist', BASE_THRESHOLDS['moist'] - BUFFER),
        ('wet', -math.inf),
    ],
    'wet': [
        ('very-dry', BASE_THRESHOLDS['very-dry']),
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist'] + BUFFER),
        ('wet', -math.inf),
    ]
}


class Sensor():
    def __init__(self):
        self.moisture = None
        self.thresholds = BASE_THRESHOLDS

        self._update_cb = None
        self._interval = INTERVAL
        self._moisture_sensor = GroveMoistureSensor(0)
        self._last_readings = []

    def on_update(self, update_cb):
        self._update_cb = update_cb

    def update(self):
        moisture, mean_moisture = self.read_moisture()
        logging.info("sensor: time: {0}, moisture level: {1}, mean moisture level: {2}".format(
            datetime.utcnow(), moisture, mean_moisture))
        self.moisture = moisture
        self.mean_moisture = mean_moisture

        self._update_cb(self.moisture, self.mean_moisture)

    async def update_loop(self):
        while 1:
            self.update()
            await asyncio.sleep(self._interval)

    def get_rolling_mean(self, reading, num_samples):
        self._last_readings.append(reading)
        self._last_readings = self._last_readings[-num_samples:]
        return sum(self._last_readings) / len(self._last_readings)

    def read_moisture(self):
        moisture = self._moisture_sensor.moisture
        mean_moisture = self.get_rolling_mean(
            moisture, NUM_MEAN_MOISTURE_SAMPLES)
        return moisture, mean_moisture
