#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import logging
from sensor import Sensor
from display import Display

logging.basicConfig(level=logging.INFO)


async def main():
    display = Display()
    sensor = Sensor(display)

    await sensor.update_loop()

asyncio.run(main())
