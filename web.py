import logging
import asyncio
from datetime import datetime, timedelta
from aiohttp import web


async def index(request):
    return web.FileResponse(path='public/index.html')


async def database(request):
    return web.FileResponse(path='database.db')


def floor_date(date, resolution):
    date = date.replace(microsecond=0, second=0)
    if resolution == "hour":
        date = date.replace(minute=0)
    elif resolution == "day":
        date = date.replace(minute=0, hour=0)
    return date


def format_start(start, resolution):
    return floor_date(datetime.fromisoformat(str(start).replace('Z', '')), resolution).isoformat()


def format_end(end, resolution):
    date = datetime.fromisoformat(str(end).replace('Z', ''))
    if resolution == "minute":
        date += timedelta(minutes=1)
    elif resolution == "hour":
        date += timedelta(hours=1)
    elif resolution == "day":
        date += timedelta(days=1)
    return floor_date(date, resolution).isoformat()


async def history(request):
    resolution = request.query['resolution'] if 'resolution' in request.query else 'day'
    start = format_start(request.query['start'] if 'start' in request.query else datetime.now(
    ) - timedelta(days=7), resolution)
    end = format_end(
        request.query['end'] if 'end' in request.query else datetime.now(), resolution)
    return web.json_response({
        'start': start,
        'end': end,
        'resolution': resolution,
        'data': request.app['db'].get_moisture_stats(start, end, resolution)
    })


def status(request):
    return web.json_response({
        'moisture': request.app['sensor'].moisture,
        'state': request.app['state_manager'].state,
        'base_state': request.app['state_manager'].base_state,
    })


def config(request):
    return web.json_response({
        'thresholds': request.app['state_manager'].thresholds,
    })


class PlantWebServer():
    def __init__(self, port=8080):
        self.port = port
        self._app = web.Application()
        self._app.add_routes([
            web.get('/', index),
            web.get('/history', history),
            web.get('/status', status),
            web.get('/config', config),
            web.static('/images', 'images'),
            web.static('/', 'public')])

    @property
    def db(self):
        return self._app['db']

    @db.setter
    def db(self, db):
        self._app['db'] = db

    @property
    def sensor(self):
        return self._app['sensor']

    @sensor.setter
    def sensor(self, sensor):
        self._app['sensor'] = sensor

    @property
    def state_manager(self):
        return self._app['state_manager']

    @state_manager.setter
    def state_manager(self, state_manager):
        self._app['state_manager'] = state_manager

    async def start(self):
        runner = web.AppRunner(self._app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        logging.info(f"web server started on port {self.port}")
        while 1:
            await asyncio.sleep(1)


if __name__ == "__main__":
    from database import Database
    db = Database()
    db.setup()

    class FauxSensor():
        def __init__(self):
            self.moisture = 1700

    class FauxStateManager():
        def __init__(self):
            self.state = 'cap'
            self.base_state = 'wet'
            self.thresholds = {
                'very-dry': 1550,
                'dry': 1500,
                'moist': 1410,
            }

    faux_sensor = FauxSensor()
    faux_state_manager = FauxStateManager()

    loop = asyncio.get_event_loop()
    try:
        plant_web_server = PlantWebServer()
        plant_web_server.db = db
        plant_web_server.sensor = faux_sensor
        plant_web_server.state_manager = faux_state_manager
        loop.run_until_complete(plant_web_server.start())
    except KeyboardInterrupt:
        pass
    loop.close()
