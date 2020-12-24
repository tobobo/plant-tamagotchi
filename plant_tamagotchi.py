#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import logging
from sensor import Sensor
from display import Display
from database import Database

logging.basicConfig(level=logging.INFO)


async def main():
    db = Database()
    db.setup()
    display = Display()
    sensor = Sensor(display, db)

    await sensor.update_loop()

asyncio.run(main())
