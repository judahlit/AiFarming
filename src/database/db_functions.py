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
    
conn = None
def insert_blood_sampling_data(id, sex, country, coat_color):
    global conn
    
    
    if (conn is None):
        conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # check if animal id already exists
    c.execute('SELECT * FROM cow WHERE id = ?', (id,))
    if c.fetchone() is not None:
        print('Animal with id:', id, 'already exists in the database, updating')
        c.execute('UPDATE cow SET sex = ?, country = ?, coat_color = ? WHERE id = ?', (sex, country, coat_color, id))
        return
    
    
    c.execute('INSERT INTO cow (id, sex, country, coat_color) VALUES (?, ?, ?, ?)', (id, sex, country, coat_color))
    
    
def commit():
    conn.commit()
    conn.close()


def insert_slaughter_data(id, birth_date, slaughter_date, lifetime_days, slaughter_weight):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # check if animal id already exists
    c.execute('SELECT * FROM cows WHERE id = ?', (id,))
    if c.fetchone() is not None:
        print('Animal with id:', id, 'already exists in the database, updating')
        c.execute(
            'UPDATE cows SET birth_date = ?, slaughter_date = ?, lifetime_days = ?, slaughter_weight = ? WHERE id = ?',
            (birth_date, slaughter_date, lifetime_days, slaughter_weight, id)
        )
        return
    
    c.execute(
        'INSERT INTO cows (id, sex, country, coat_color, birth_date, slaughter_date, lifetime_days, slaughter_weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (id, None, None, None, birth_date, slaughter_date, lifetime_days, slaughter_weight)
    )
    
    conn.commit()
    conn.close()