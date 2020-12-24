import sqlite3

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
