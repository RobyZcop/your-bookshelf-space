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
        takeaways TEXT,
        UNIQUE(title, author)
    );
    """)
    print("Created table: books")


# Create users_books table if does not exist
if not table_exists("users_books"):
    db.execute("""
    CREATE TABLE users_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, book_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    );
    """)
    print("Created table: users_books")

# Create notes table if does not exist
if not table_exists("notes"):
    db.execute("""
    CREATE TABLE notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        note TEXT,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    );
    """)
    print("Created table: notes")


# Create quote table if does not exist
if not table_exists("quotes"):
    db.execute("""
    CREATE TABLE quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        quote TEXT
    );
    """)
    print("Created table: quotes")

