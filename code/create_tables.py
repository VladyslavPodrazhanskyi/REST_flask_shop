import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)


create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO items VALUES ('test_item', 10.99)")   # test insert before code put method for items

connection.commit()
connection.close()

# create_table = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"

