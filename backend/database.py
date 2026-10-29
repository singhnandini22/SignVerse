import sqlite3


DATABASE = "backend/signverse.db"


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# -----------------------------------------
# CREATE / UPDATE USERS TABLE
# -----------------------------------------

def create_users_table():

    connection = get_connection()

    cursor = connection.cursor()


    # Create users table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            phone TEXT,
            age INTEGER,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            letters_progress INTEGER DEFAULT 0,
            numbers_progress INTEGER DEFAULT 0
        )
    """)


    # Get existing columns
    cursor.execute("PRAGMA table_info(users)")

    columns = cursor.fetchall()

    column_names = [column["name"] for column in columns]


    # Add phone column if it does not exist
    if "phone" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN phone TEXT
        """)


    # Add age column if it does not exist
    if "age" not in column_names:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN age INTEGER
        """)


    connection.commit()

    connection.close()