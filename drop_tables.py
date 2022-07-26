import sqlite3

conn = sqlite3.connect('properties.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE properties
          ''')

conn.commit()
conn.close()
