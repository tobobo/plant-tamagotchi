import os
import logging
import time
import asyncio
import traceback
import math
from PIL import Image, ImageDraw, ImageFont
from aiolimiter import AsyncLimiter
from lib.epd2in13bc import EPD

image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

MIN_COOLDOWN = 15
MIN_MEAN_INTERVAL = 180
INTERVAL_HISTORY_LENGTH = 5
BACKOFF_MULTIPLIER = 2


class Display():
    def __init__(self):
        self.last_update = None
        self.state = None
        self.comitted_state = None
        self.debounce_task = None
        self.recent_intervals = []

    def update(self, state):
        self.state = state

        if self.debounce_task == None or self.debounce_task.done():
            logging.debug("creating task")
            self.debounce_task = asyncio.create_task(
                self.debounce_commit(MIN_COOLDOWN))
        else:
            logging.info("debounced display update: time: {0}, state: {1}".format(
                time.time(), state))

    async def debounce_commit(self, backoff):
        if self.comitted_state != self.state:
            now = time.time()
            last_update = self.record_interval(now)
            cooldown = self.get_cooldown(backoff)
            logging.info("display update: time: {0}, last state: {1}, current state: {2}, last update: {3}, cooldown: {4}".format(
                now, self.comitted_state, self.state, last_update, cooldown))
            self.comitted_state = self.state
            await asyncio.gather(self.draw(), asyncio.sleep(cooldown))
            logging.debug("Cooldown complete")
            await self.debounce_commit(backoff * BACKOFF_MULTIPLIER)

    def record_interval(self, time):
        last_update = self.last_update
        if last_update != None:
            self.recent_intervals.append(time - last_update)
            self.recent_intervals = self.recent_intervals[-INTERVAL_HISTORY_LENGTH:]
        self.last_update = time
        return last_update

    def get_cooldown(self, backoff):
        if len(self.recent_intervals) < INTERVAL_HISTORY_LENGTH:
            return backoff

        mean_update_interval = self.get_mean_update_interval()
        if mean_update_interval >= MIN_MEAN_INTERVAL:
            return backoff
        else:
            return (INTERVAL_HISTORY_LENGTH + 1) * MIN_MEAN_INTERVAL - INTERVAL_HISTORY_LENGTH * mean_update_interval

    def get_mean_update_interval(self):
        if len(self.recent_intervals) == 0:
            return None
        else:
            return sum(self.recent_intervals) / len(self.recent_intervals)

    async def draw(self):
        try:
            epd = EPD()
            await epd.init()

            logging.debug("Drawing status {0}".format(self.state))
            blackimage1 = Image.new(
                '1', (epd.height, epd.width), 255)  # 298*126
            redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
            plant = Image.open(os.path.join(
                image_dir, self.state + '.png'))
            rotated = plant.transpose(Image.ROTATE_90)
            width, height = rotated.size
            enlarged = rotated.resize((width * 4, height * 4))
            new_width, new_height = enlarged.size
            blackimage1.paste(enlarged, (round(
                (epd.height - new_width) / 2), round((epd.width - new_height) / 2)))
            await epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

            logging.debug("Display sleep...")
            await epd.sleep()
            await asyncio.sleep(3)
            epd.dev_exit()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd.dev_exit()
            exit()
