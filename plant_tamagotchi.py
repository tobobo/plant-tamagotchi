#!/usr/bin/python
# -*- coding:utf-8 -*-
import asyncio
import logging
from sensor import Sensor
from display import Display
from database import Database
from state_manager import StateManager
from mediator import Mediator
from web import PlantWebServer

logging.basicConfig(level=logging.INFO)


async def main():
    db = Database()
    db.setup()

    sensor = Sensor()
    state_manager = StateManager()
    display = Display()

    mediator = Mediator()
    mediator.db = db
    mediator.sensor = sensor
    mediator.state_manager = state_manager
    mediator.display = display
    mediator.bind_updaters()

    web_server = PlantWebServer(port=80)
    web_server.db = db
    web_server.sensor = sensor
    web_server.state_manager = state_manager

    asyncio.create_task(web_server.start())

    await sensor.update_loop()

asyncio.run(main())
