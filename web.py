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


def format_start(end, resolution):
    return floor_date(end, resolution).isoformat()


def format_end(start, resolution):
    date = start
    if resolution == "minute":
        date += timedelta(minutes=1)
    elif resolution == "hour":
        date += timedelta(hours=1)
    elif resolution == "day":
        date += timedelta(days=1)
    return floor_date(date, resolution).isoformat()


async def moisture(request):
    resolution = request.query['resolution'] if 'resolution' in request.query else 'day'
    start = format_start(request.query['start'] if 'start' in request.query else datetime.now(
    ) - timedelta(weeks=2), resolution)
    end = format_end(
        request.query['end'] if 'end' in request.query else datetime.now(), resolution)
    return web.json_response({
        'start': start,
        'end': end,
        'resolution': resolution,
        'data': request.app['db'].get_moisture_stats(start, end, resolution)
    })


async def start_server(db):
    app = web.Application()
    app.add_routes([
        web.get('/', index),
        web.get('/moisture', moisture),
        web.static('/', 'public')])
    app['db'] = db
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    while 1:
        await asyncio.sleep(1)


if __name__ == "__main__":
    from database import Database
    db = Database()
    db.setup()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server(db))
    except KeyboardInterrupt:
        pass
    loop.close()
