import asyncio
import logging
import time
from datetime import datetime
import os
import sys
import math
from lib.moisture_sensor import GroveMoistureSensor

INTERVAL = 5

MOISTURE_THRESHOLDS = {
    None: [
        ('dry', 1900),
        ('moist', 1650),
        ('wet', -math.inf),
    ],
    'dry': [
        ('dry', 1850),
        ('moist', 1650),
        ('wet', -math.inf)
    ],
    'moist': [
        ('dry', 1950),
        ('moist', 1600),
        ('wet', -math.inf),
    ],
    'wet': [
        ('dry', 1900),
        ('moist', 1700),
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

    def update(self):
        now = time.time()
        moisture, state = self.read_moisture()
        logging.info("sensor: time: {0}, moisture level: {1}, previous state: {2}, current state: {3}".format(
            now, moisture, self.state, state))
        self.db.write_moisture(datetime.now().isoformat(), moisture, state)
        if self.state != state:
            self.display.update(state)
        self.state = state
        self.moisture = moisture

    async def update_loop(self):
        while 1:
            self.update()
            await asyncio.sleep(self.interval)

    def read_moisture(self):
        moisture = self.moisture_sensor.moisture
        for state, threshold in MOISTURE_THRESHOLDS[self.state]:
            if moisture > threshold:
                return moisture, state
