from cs50 import SQL

# Connect to existing database
db = SQL("sqlite:///books.db")

# Function to check if a table exist
def table_exists(table_name):
    result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", table_name)
    return len(result) > 0

# Create users table if does not exists
if not table_exists("users"):
    db.execute(""" 
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    );
    """)
    print("Created table: users")

# Create books table if does not exists
if not table_exists("books"):
    db.execute(""" 
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        publication_year INTEGER,
        rating NUMERIC,
        date_read TEXT,
        status TEXT,
        takeaways TEXT
    );
    """)
    print("Created table: books")
