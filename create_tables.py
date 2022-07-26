import sqlite3

conn = sqlite3.connect('properties.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE properties
          (id INTEGER PRIMARY KEY ASC, 
           parcel_number VARCHAR(100) NOT NULL,
           street_name VARCHAR(100) NOT NULL,
           city VARCHAR(100) NOT NULL,
           postal_code INTEGER NOT NULL,
           purchase_price VARCHAR(100) NOT NULL,
           selling_price FLOAT NOT NULL,
           is_sold FLOAT,
           type VARCHAR(100) NOT NULL,
           hoa_fee INTEGER,
           developer_name VARCHAR(100),
           unit INTEGER,
           strata_fee INTEGER,
           square_footage INTEGER,
           number_active_tenants INTEGER) 
          ''')

conn.commit()
conn.close()
