import sqlite3

conn = sqlite3.connect('home_data.db')
cursor = conn.cursor()
create_table_query = '''
    CREATE TABLE IF NOT EXISTS home_data (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        icon TEXT NOT NULL,
        price FLOAT NOT NULL
    )
'''

cursor.execute(create_table_query)

conn.commit()
conn.close()
