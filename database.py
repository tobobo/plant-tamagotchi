import sqlite3

formats = {
  "day": "%Y-%m-%dT00:00:00Z",
  "hour": "%Y-%m-%dT%H:00:00Z",
  "minute": "%Y-%m-%dT%H:%M:00Z",
}

class Database:
  def __init__(self):
    self.conn = sqlite3.connect("database.db")
  
  def setup(self):
    c = self.conn.cursor()
    c.execute('''
      CREATE TABLE IF NOT EXISTS moisture
      (datetime TEXT UNIQUE, moisture INT, state TEXT)
    ''')
    self.conn.commit()

  def write_moisture(self, datetime, moisture, state):
    c = self.conn.cursor()
    c.execute('INSERT INTO moisture VALUES (?, ?, ?)', (datetime, moisture, state))
    self.conn.commit()
    
  def get_moisture(self):
    c = self.conn.cursor()
    c.execute('SELECT * FROM moisture')
    return c.fetchall()
    
  def get_moisture_stats(self, start, end, resolution):
    c = self.conn.cursor()
    c.execute('''
      select
      strftime(?, datetime) as group_time,
      avg(moisture)
      from moisture
      where datetime >= ?
      and datetime < ?
      group by group_time
      order by group_time asc;
    ''', (formats[resolution], start, end))
    return c.fetchall()
