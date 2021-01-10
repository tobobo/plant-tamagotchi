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
        'state': request.app['sensor'].state
    })


async def start_server(db, sensor, port=8080):
    app = web.Application()
    app.add_routes([
        web.get('/', index),
        web.get('/history', history),
        web.get('/status', status),
        web.static('/images', 'images'),
        web.static('/', 'public')])
    app['db'] = db
    app['sensor'] = sensor
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info("web server started on port {0}".format(port))
    while 1:
        await asyncio.sleep(1)


if __name__ == "__main__":
    from database import Database
    db = Database()
    db.setup()

    class FauxSensor():
        def __init__(self):
            self.moisture = 1700
            self.state = 'wet'

    faux_sensor = FauxSensor()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server(db, faux_sensor))
    except KeyboardInterrupt:
        pass
    loop.close()
