import sqlite3
from datetime import datetime

formats = {
    "day": "%Y-%m-%dT00:00:00Z",
    "hour": "%Y-%m-%dT%H:00:00Z",
    "minute": "%Y-%m-%dT%H:%M:00Z",
}

rollup_tables = {
    "day": "moisture_day",
    "hour": "moisture_hour",
    "minute": "moisture_minute",
}


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")

    def setup(self):
        c = self.conn.cursor()
        c.execute('''
      CREATE TABLE IF NOT EXISTS moisture
      (datetime TEXT UNIQUE, moisture INT, state TEXT);
        ''')
        c.execute('''
      CREATE TABLE IF NOT EXISTS moisture_day
      (datetime TEXT UNIQUE, moisture INT, samples INT);
        ''')
        c.execute('''
      CREATE TABLE IF NOT EXISTS moisture_hour
      (datetime TEXT UNIQUE, moisture INT, samples INT);
        ''')
        c.execute('''
      CREATE TABLE IF NOT EXISTS moisture_minute
      (datetime TEXT UNIQUE, moisture INT, samples INT);
        ''')
        self.conn.commit()

    def insert_to_rollup_table(self, c, rollup, timestamp, moisture):
        c.execute(f'''
            INSERT INTO {rollup_tables[rollup]} (datetime, moisture, samples) VALUES (strftime(?, ?), ?, 1)
            ON CONFLICT(datetime) DO UPDATE SET
            moisture = (moisture * samples + excluded.moisture) / (samples + 1),
            samples = samples + 1
        ''', (formats[rollup], timestamp, moisture))

    def write_moisture(self, moisture, state, timestamp=None):
        if timestamp == None:
            timestamp = datetime.now()

        c = self.conn.cursor()
        c.execute('INSERT INTO moisture (datetime, moisture, state) VALUES (?, ?, ?)',
                  (timestamp.isoformat(), moisture, state))
        self.insert_to_rollup_table(c, "day", timestamp, moisture)
        self.insert_to_rollup_table(c, "hour", timestamp, moisture)
        self.insert_to_rollup_table(c, "minute", timestamp, moisture)
        self.conn.commit()

    def get_moisture(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM moisture')
        return c.fetchall()

    def get_moisture_stats(self, start, end, resolution):
        c = self.conn.cursor()
        c.execute(f'''
        select datetime, moisture from {rollup_tables[resolution]}
        where datetime >= ? and datetime < ?
        order by datetime asc
        ''', (start, end))
        return c.fetchall()
