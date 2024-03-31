import sqlite3

conn = sqlite3.connect('shopping_info.db')
cursor = conn.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS shopping_info (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
'''
cursor.execute(create_table_query)

conn.commit()
conn.close()
