import os
import logging
import time
import asyncio
import traceback
import math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from lib.epd2in13bc import EPD

image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

MIN_COOLDOWN = 15
MIN_MEAN_INTERVAL = 180
INTERVAL_HISTORY_LENGTH = 5
BACKOFF_MULTIPLIER = 2

DEFAULT_SCALE = 4

STATE_SCALE = {
    'brushing_teeth': 3
}


class Display():
    def __init__(self):
        self._last_update = None
        self._state = None
        self._comitted_state = None
        self._debounce_task = None
        self._recent_intervals = []

    def update(self, state, moisture):
        if self._state != state:
            self._state = state

            if self._debounce_task == None or self._debounce_task.done():
                logging.debug("creating task")
                self._debounce_task = asyncio.create_task(
                    self.debounce_commit(MIN_COOLDOWN))
            else:
                logging.info("debounced display update: time: {0}, state: {1}".format(
                    datetime.now(), state))

    async def debounce_commit(self, backoff):
        if self._comitted_state != self._state:
            now = time.time()
            last_update = self.record_interval(now)
            cooldown = self.get_cooldown(backoff)
            logging.info("display update: time: {0}, last state: {1}, current state: {2}, last update: {3}, cooldown: {4}".format(
                datetime.utcnow(), self._comitted_state, self._state, last_update, cooldown))
            self._comitted_state = self._state
            await asyncio.gather(self.draw(), asyncio.sleep(cooldown))
            logging.debug("Cooldown complete")
            await self.debounce_commit(backoff * BACKOFF_MULTIPLIER)

    def record_interval(self, time):
        last_update = self._last_update
        if last_update != None:
            self._recent_intervals.append(time - last_update)
            self._recent_intervals = self._recent_intervals[-INTERVAL_HISTORY_LENGTH:]
        self._last_update = time
        return last_update

    def get_cooldown(self, backoff):
        if len(self._recent_intervals) < INTERVAL_HISTORY_LENGTH:
            return backoff

        mean_update_interval = self.get_mean_update_interval()
        if mean_update_interval >= MIN_MEAN_INTERVAL:
            return backoff
        else:
            return (INTERVAL_HISTORY_LENGTH + 1) * MIN_MEAN_INTERVAL - INTERVAL_HISTORY_LENGTH * mean_update_interval

    def get_mean_update_interval(self):
        if len(self._recent_intervals) == 0:
            return None
        else:
            return sum(self._recent_intervals) / len(self._recent_intervals)

    def get_scale(self, state):
        if state in STATE_SCALE:
            return STATE_SCALE[state]
        else:
            return DEFAULT_SCALE

    async def draw(self):
        try:
            epd = EPD()
            await epd.init()

            logging.debug("Drawing status {0}".format(self._state))
            blackimage1 = Image.new(
                '1', (epd.height, epd.width), 255)  # 298*126
            redimage1 = Image.new('1', (epd.height, epd.width), 255)  # 298*126
            plant = Image.open(os.path.join(
                image_dir, self._state + '.png'))
            rotated = plant.transpose(Image.ROTATE_90)
            width, height = rotated.size
            scale = self.get_scale(self._state)
            enlarged = rotated.resize((width * scale, height * scale))
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
