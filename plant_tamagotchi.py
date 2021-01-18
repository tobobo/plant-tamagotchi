#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import logging
from sensor import Sensor
from display import Display
from database import Database
from fun_display_proxy import FunDisplayProxy
from web import start_server

logging.basicConfig(level=logging.INFO)


async def main():
    db = Database()
    db.setup()
    display = Display()
    fun_display_proxy = FunDisplayProxy(display)
    sensor = Sensor(fun_display_proxy, db)

    asyncio.create_task(start_server(port=80, db=db, sensor=fun_display_proxy))

    await sensor.update_loop()

asyncio.run(main())
