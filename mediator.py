class Mediator():
    def __init__(self):
        self.db = None
        self.display = None
        self.state_manager = None
        self.sensor = None

    def bind_updaters(self):
        self.sensor.on_update(self.handle_moisture_update)
        self.state_manager.on_update(self.handle_state_moisture_update)

    def handle_moisture_update(self, moisture, mean_moisture):
        self.state_manager.update(moisture, mean_moisture)

    def handle_state_moisture_update(self, state, base_state, moisture):
        self.db.write_moisture(moisture, base_state)
        self.display.update(state, moisture)
