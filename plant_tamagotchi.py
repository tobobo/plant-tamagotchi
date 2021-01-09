#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import logging
import threading
from sensor import Sensor
from display import Display
from database import Database
from web import start_server

logging.basicConfig(level=logging.INFO)


async def main():
    db = Database()
    db.setup()
    display = Display()
    sensor = Sensor(display, db)

    asyncio.create_task(start_server(port=80, db=db, sensor=sensor))

    await sensor.update_loop()

asyncio.run(main())
