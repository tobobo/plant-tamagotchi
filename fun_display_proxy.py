from datetime import datetime, date, time
from random import random, randrange

PROXY_STATES = ['cap', 'computer', 'music', 'skateboard', 'wig']
MORNING_BRUSH_HOUR = 9
EVENING_BRUSH_HOUR = 21
CHANCE_OF_FUN_STATE = 0.3

class FunDisplayProxy():
    def __init__(self, display):
        self.display = display
        self.moisture = None
        self.state = None
        self.base_state = None
        self.proxy_state = None
        self.proxy_state_date = None

    def update(self, state, moisture):
        self.moisture = moisture
        if state != 'moist':
            self.base_state = state
            self.state = state
            self.display.update(self.state, self.moisture)
        else:
            time_based_state = self.get_time_based_state()
            if time_based_state != None:
                self.state = time_based_state
                self.base_state = state
                self.display.update(self.state, self.moisture)
            elif (state == self.base_state and self.proxy_state != None and self.proxy_state_date == date.today()):
                self.state = self.proxy_state
                self.display.update(self.proxy_state, self.moisture)
            else:
                self.proxy_state_date = date.today()
                self.state = self.get_proxy_state(state)
                self.proxy_state = self.state
                self.base_state = state
                self.display.update(self.state, self.moisture)

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
