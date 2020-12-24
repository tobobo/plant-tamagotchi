import os
import logging
import time
import asyncio
import traceback
from PIL import Image, ImageDraw, ImageFont
from lib.epd2in13bc import EPD

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

SHORT_INTERVAL = 15
LONG_INTERVAL = 180


class Display():
    def __init__(self, sensor):
        self.sensor = sensor
        self.interval = SHORT_INTERVAL
        self.recent_intervals = []
        self.last_update = None
        self.state = None

    async def update(self):
        now = time.time()
        logging.info("time: {0}, last update: {1}, last intervals: {2}, draw delay: {3}".format(
            now, self.last_update, self.recent_intervals, self.interval))
        if self.sensor.state != self.state:
            if self.last_update != None:
                self.recent_intervals.append(now - self.last_update)
                self.recent_intervals = self.recent_intervals[-5:]
                if (self.has_done_too_many_updates()):
                    self.interval = LONG_INTERVAL
                else:
                    self.interval = self.interval * 2
            self.last_update = now
            self.state = self.sensor.state
            await self.draw()
        else:
            self.interval = SHORT_INTERVAL

    async def update_loop(self):
        while 1:
            await self.update()
            await asyncio.sleep(self.interval)

    def has_done_too_many_updates(self):
        return len(self.recent_intervals) > 5 and sum(self.recent_intervals) / len(self.recent_intervals) < LONG_INTERVAL

    async def draw(self):
        try:
            epd = EPD()
            await epd.init()

            logging.info("Drawing status {0}".format(self.state))
            blackimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
            redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
            plant = Image.open(os.path.join(picdir, self.state + '.png'))
            rotated = plant.transpose(Image.ROTATE_90)
            width, height = rotated.size
            enlarged = rotated.resize((width * 4, height * 4))
            new_width, new_height = enlarged.size
            blackimage1.paste(enlarged, (round(
                (epd.height - new_width) / 2), round((epd.width - new_height) / 2)))
            await epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

            logging.info("Display sleep...")
            await epd.sleep()
            await asyncio.sleep(3)
            epd.dev_exit()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd.dev_exit()
            exit()
