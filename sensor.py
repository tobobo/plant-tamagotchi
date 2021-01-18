import asyncio
import logging
import time
from datetime import datetime
import os
import sys
import math
from lib.moisture_sensor import GroveMoistureSensor

INTERVAL = 5

BASE_THRESHOLDS = {
    'dry': 1500,
    'moist': 1410,
}

BUFFER = 5

NUM_MEAN_MOISTURE_SAMPLES = 10

MOISTURE_THRESHOLDS = {
    None: [
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf),
    ],
    'dry': [
        ('dry', BASE_THRESHOLDS['dry'] - BUFFER),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf)
    ],
    'moist': [
        ('dry', BASE_THRESHOLDS['dry'] + BUFFER),
        ('moist', BASE_THRESHOLDS['moist'] - BUFFER),
        ('wet', -math.inf),
    ],
    'wet': [
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist'] + BUFFER),
        ('wet', -math.inf),
    ]
}


class Sensor():
    def __init__(self, display, db):
        self.display = display
        self.db = db
        self.interval = INTERVAL
        self.moisture_sensor = GroveMoistureSensor(0)
        self.moisture = None
        self.state = None
        self.last_readings = []

    def update(self):
        now = time.time()
        moisture, mean_moisture, state = self.read_moisture()
        logging.info("sensor: time: {0}, moisture level: {1}, mean moisture level: {2}, previous state: {3}, current state: {4}".format(
            now, moisture, mean_moisture, self.state, state))
        self.db.write_moisture(datetime.now().isoformat(), moisture, state)
        self.display.update(state, moisture)
        self.state = state
        self.moisture = moisture
        self.mean_moisture = mean_moisture

    async def update_loop(self):
        while 1:
            self.update()
            await asyncio.sleep(self.interval)

    def get_rolling_mean(self, reading, num_samples):
        self.last_readings.append(reading)
        self.last_readings = self.last_readings[-num_samples:]
        return sum(self.last_readings) / len(self.last_readings)

    def read_moisture(self):
        moisture = self.moisture_sensor.moisture
        mean_moisture = self.get_rolling_mean(
            moisture, NUM_MEAN_MOISTURE_SAMPLES)
        for state, threshold in MOISTURE_THRESHOLDS[self.state]:
            if mean_moisture > threshold:
                return moisture, mean_moisture, state
