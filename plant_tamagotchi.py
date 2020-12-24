#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import logging
from sensor import Sensor
from display import Display

logging.basicConfig(level=logging.INFO)


async def main():
    sensor = Sensor()
    display = Display(sensor)

    sensor.update()
    await asyncio.gather(sensor.update_loop(), display.update_loop())

asyncio.run(main())
