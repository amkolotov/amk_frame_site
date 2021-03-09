import sqlite3

conn = sqlite3.connect('site.sqlite')
cursor = conn.cursor()

with open('create_db.sql', 'r') as file:
    text = file.read()
cursor.executescript(text)

cursor.close()
conn.close()
