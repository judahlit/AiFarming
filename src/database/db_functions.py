import sqlite3

def build_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # execute sql file
    with open('src/database/schema.sql', 'r') as f:
        sql = f.read()
        c.executescript(sql)

    conn.commit()
    conn.close()
    
def delete_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # execute sql file
    with open('src/database/delete.sql', 'r') as f:
        sql = f.read()
        c.executescript(sql)

    conn.commit()
    conn.close()
    
    
def insert_blood_sampling_data(data):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.executemany('INSERT INTO blood_sampling_data VALUES (