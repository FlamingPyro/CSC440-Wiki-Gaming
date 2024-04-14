import sqlite3

conn = sqlite3.connect('comments_db.py')
cursor = conn.cursor()
create_table_query= '''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_table_query)

conn.commit()
conn.close()
