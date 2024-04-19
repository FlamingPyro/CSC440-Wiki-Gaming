import sqlite3

conn = sqlite3.connect('comments_db.py')
cursor = conn.cursor()

create_destiny_table_query= '''
CREATE TABLE IF NOT EXISTS destiny (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_destiny_table_query)

create_lethalcompany_table_query= '''
CREATE TABLE IF NOT EXISTS lethalcompany (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_lethalcompany_table_query)

create_minecraft_table_query= '''
CREATE TABLE IF NOT EXISTS minecraft (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_minecraft_table_query)

create_tekken8_table_query= '''
CREATE TABLE IF NOT EXISTS tekken8 (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_tekken8_table_query)

create_eldenring_table_query= '''
CREATE TABLE IF NOT EXISTS eldenring (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_eldenring_table_query)

create_palworlds_table_query= '''
CREATE TABLE IF NOT EXISTS palworld (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_palworlds_table_query)

create_horizonforbiddenwest_table_query= '''
CREATE TABLE IF NOT EXISTS horizonforbiddenwest (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_horizonforbiddenwest_table_query)

create_helldivers_table_query= '''
CREATE TABLE IF NOT EXISTS helldivers (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    comments TEXT NOT NULL,
    numLikes TEXT NOT NULL
)

'''
cursor.execute(create_helldivers_table_query)

create_shopping_table_query = '''
CREATE TABLE IF NOT EXISTS shopping_info (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
'''
cursor.execute(create_shopping_table_query)

create_game_table_query = '''
    CREATE TABLE IF NOT EXISTS home_data (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        icon TEXT NOT NULL,
        price FLOAT NOT NULL
    )
'''


cursor.execute(create_game_table_query)
conn.commit()
conn.close()

