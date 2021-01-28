import os
import math
import logging
from datetime import datetime, date, time
from random import random, randrange

PROXY_STATES = ['cap', 'computer', 'music', 'skateboard', 'wig']
MORNING_BRUSH_HOUR = 9
EVENING_BRUSH_HOUR = 21
CHANCE_OF_FUN_STATE = 0.3

FORCED_FUN_STATE_PATH = './forced_fun_state'

BASE_THRESHOLDS = {
    'very-dry': 1550,
    'dry': 1500,
    'moist': 1410,
}

BUFFER = 5

MOISTURE_THRESHOLDS = {
    None: [
        ('very-dry', BASE_THRESHOLDS['very-dry']),
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf),
    ],
    'very-dry': [
        ('very-dry', BASE_THRESHOLDS['very-dry'] - BUFFER),
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf)
    ],
    'dry': [
        ('very-dry', BASE_THRESHOLDS['very-dry'] + BUFFER),
        ('dry', BASE_THRESHOLDS['dry'] - BUFFER),
        ('moist', BASE_THRESHOLDS['moist']),
        ('wet', -math.inf)
    ],
    'moist': [
        ('very-dry', BASE_THRESHOLDS['very-dry']),
        ('dry', BASE_THRESHOLDS['dry'] + BUFFER),
        ('moist', BASE_THRESHOLDS['moist'] - BUFFER),
        ('wet', -math.inf),
    ],
    'wet': [
        ('very-dry', BASE_THRESHOLDS['very-dry']),
        ('dry', BASE_THRESHOLDS['dry']),
        ('moist', BASE_THRESHOLDS['moist'] + BUFFER),
        ('wet', -math.inf),
    ]
}


class StateManager():
    def __init__(self):
        self.state = None
        self.base_state = None
        self.thresholds = BASE_THRESHOLDS

        self._update_cb = None
        self._proxy_state = None
        self._proxy_state_date = None
        self.set_forced_fun_state()

    def set_forced_fun_state(self):
        try:
            with open(FORCED_FUN_STATE_PATH) as f:
                self._forced_fun_state = f.read().strip()
            os.remove(FORCED_FUN_STATE_PATH)
        except Exception:
            self._forced_fun_state = None

    def on_update(self, update_cb):
        self._update_cb = update_cb

    def get_base_state(self, moisture):
        for state, threshold in MOISTURE_THRESHOLDS[self.base_state]:
            if moisture > threshold:
                return state

    def update_state(self, base_state):
        if base_state != 'moist':
            self.state = base_state
        else:
            time_based_state = self.get_time_based_state()
            if time_based_state != None:
                self.state = time_based_state
            elif (self._forced_fun_state != None):
                self.state = self._forced_fun_state
                self._proxy_state = self.state
                self._proxy_state_date = date.today()
                self._forced_fun_state = None
            elif (base_state == self.base_state and self._proxy_state != None and self._proxy_state_date == date.today()):
                self.state = self._proxy_state
            else:
                self.state = self.get_proxy_state(base_state)
                self._proxy_state = self.state
                self._proxy_state_date = date.today()

    def update(self, moisture, mean_moisture):
        base_state = self.get_base_state(mean_moisture)
        self.update_state(base_state)

        self.base_state = base_state
        logging.info("state_manager: time: {0}, state: {1}, base state: {2}".format(
            datetime.utcnow(), self.state, base_state))
        self._update_cb(self.state, self.base_state, moisture)

    def get_time_based_state(self):
        current_time = datetime.now().time()
        # between 9 and 9:10, am or pm
        if (current_time > time(MORNING_BRUSH_HOUR) and current_time < time(MORNING_BRUSH_HOUR, 10)) or \
                (current_time > time(EVENING_BRUSH_HOUR) and current_time < time(EVENING_BRUSH_HOUR, 10)):
            return 'brushing_teeth'
        else:
            return None

    def get_proxy_state(self, state):
        if (1 - random() < CHANCE_OF_FUN_STATE):
            # not a fun state
            return state
        else:
            return PROXY_STATES[randrange(len(PROXY_STATES))]
