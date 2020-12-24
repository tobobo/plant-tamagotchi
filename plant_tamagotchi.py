#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import asyncio
import traceback
import time
from grove_moisture_sensor import GroveMoistureSensor
from epd.epd2in13bc import EPD
import logging
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epd')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.INFO)


def draw(status):
    try:
        epd = EPD()
        epd.init()

        logging.info("Drawing status {0}".format(status))
        blackimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        plant = Image.open(os.path.join(picdir, status + '.png'))
        rotated = plant.transpose(Image.ROTATE_90)
        width, height = rotated.size
        enlarged = rotated.resize((width * 4, height * 4))
        new_width, new_height = enlarged.size
        blackimage1.paste(enlarged, (round(
            (epd.height - new_width) / 2), round((epd.width - new_height) / 2)))
        epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

        logging.info("Display sleep...")
        epd.sleep()
        time.sleep(3)
        epd.Dev_exit()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.Dev_exit()
        exit()


def get_moisture_status(status, sensor):
    moisture = sensor.moisture
    if status == None:
        if moisture > 1900:
            return (moisture, 'dry')
        elif moisture > 1500:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
    elif status == 'dry':
        if moisture > 1850:
            return (moisture, 'dry')
        elif moisture > 1500:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
    elif status == 'moist':
        if moisture > 1950:
            return (moisture, 'dry')
        elif moisture > 1450:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')
    elif status == 'wet':
        if moisture > 1900:
            return (moisture, 'dry')
        elif moisture > 1550:
            return (moisture, 'moist')
        else:
            return (moisture, 'wet')


SENSOR_INTERVAL = 5
SHORT_DELAY = 15
LONG_DELAY = 180


def is_too_many_updates(recent_intervals):
    return len(recent_intervals) > 5 and sum(recent_intervals) / len(recent_intervals) < LONG_DELAY


class Sensor():
    def __init__(self):
        self.interval = SENSOR_INTERVAL
        self.moisture_sensor = GroveMoistureSensor(0)
        self.state = None

    def update(self):
        now = time.time()
        (moisture, state) = get_moisture_status(
            self.state, self.moisture_sensor)
        logging.info("{0} moisture level: {1}, previous state: {2}, current state: {3}".format(
            now, moisture, self.state, state))
        self.state = state

    async def update_loop(self):
        while 1:
            self.update()
            await asyncio.sleep(self.interval)


class Display():
    def __init__(self, sensor):
        self.sensor = sensor
        self.interval = SHORT_DELAY
        self.recent_intervals = []
        self.last_update = None
        self.state = None

    def update(self):
        now = time.time()
        logging.info("{0} last update: {1}, last intervals: {2}, draw delay: {3}".format(
            now, self.last_update, self.recent_intervals, self.interval))
        if self.sensor.state != self.state:
            if self.last_update != None:
                self.recent_intervals.append(now - self.last_update)
                self.recent_intervals = self.recent_intervals[-5:]
                if (is_too_many_updates(self.recent_intervals)):
                    self.interval = LONG_DELAY
                else:
                    self.interval = self.interval * 2
            self.last_update = now
            self.state = self.sensor.state
            draw(self.state)
        else:
            self.interval = SHORT_DELAY

    async def update_loop(self):
        while 1:
            self.update()
            await asyncio.sleep(self.interval)


async def main():
    sensor = Sensor()
    display = Display(sensor)

    sensor.update()
    await asyncio.gather(sensor.update_loop(), display.update_loop())

asyncio.run(main())
