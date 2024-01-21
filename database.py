import sqlite3

conn = sqlite3.connect('research.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        lab_id INTEGER,
        FOREIGN KEY (lab_id) REFERENCES labs(lab_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        text_desc TEXT,
        user_id INT NOT NULL,
        file_name TEXT,
        type TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS labs (
        lab_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lab_name TEXT NOT NULL UNIQUE
    )
''')

conn.commit()

cursor.execute("insert into labs(lab_name) values('cvit')")
cursor.execute("insert into labs(lab_name) values('precog')")
cursor.execute("insert into labs(lab_name) values('cvest')")

conn.commit()
conn.close()

print("Database 'research.db' and tables created successfully.")
