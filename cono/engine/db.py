import sqlite3

con = sqlite3.connect('cono.db')
cursor = con.cursor()


# Creating table to add system commands
query = "CREATE TABLE IF NOT EXISTS sys_commands(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# # Inserting system commands
# query = "insert into sys_commands values(null, 'acrobat', 'C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe')"
# cursor.execute(query)
# con.commit()

# Creating table to add web commands
query = "CREATE TABLE IF NOT EXISTS web_commands(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# # # Inserting web urls
# query = "insert into web_commands values(null, 'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()

# Creating table to add web commands
query = "CREATE TABLE IF NOT EXISTS web_commands(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query) 