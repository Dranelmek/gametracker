import sqlite3

conn = sqlite3.connect("WastedOnValorant.db")
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS TimeWasted
				(GameID integer PRIMARY KEY AUTOINCREMENT,
				Date Date,
				TimeWasted text)
				""")