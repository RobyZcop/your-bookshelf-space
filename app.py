from cs50 import SQL
from helpers import login_required, apology, fetch_book_details, get_daily_quote
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd 
from plotly.subplots import make_subplots
import random
import requests
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application 
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show Home Page"""

    if request.method == "GET":
        
        #Retrive user books
        user_books = db.execute(
                """
                SELECT DISTINCT
                    b.id,
                    b.title,
                    b.author, 
                    b.status,
                    ub.date_added
                FROM 
                    books AS b
                INNER JOIN 
                    users_books AS ub
                 ON b.id = ub.book_id
                WHERE
                    ub.user_id  = ?
                
                """, session["user_id"]
            )
        
        # transforming date string in actual data object so I can select the format i need in jinja
        for book in user_books:
            book["date_added"] = datetime.strptime(book["date_added"], "%Y-%m-%d %H:%M:%S")
        
        # Retrive username
        username = db.execute(
            "SELECT username from users WHERE id = ?", session["user_id"]
        )[0]
    	
        
        return render_template("index.html", user_books=user_books, username=username)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    """ User can search and add a book. """

    if request.method == "POST":
        
        # Store input inside variables
        book_title = request.form.get("book_title")
        author = request.form.get("author")
        status = request.form.get("status")
        genres = request.form.get("genres")
        
        # Validate user input
        if not book_title or not author or not status:
            return apology("All fields are required!")
        
        # Check if book already exists in the database
        book = db.execute("SELECT * FROM books WHERE title = ? AND author = ?", book_title, author)
        if not book:
            
            # Insert book into table if does not exists
            book_id = db.execute("INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, ?)", book_title, author, genres, status)
            flash("Book has been added successfully!")
        
        else:
            book_id = book[0]["id"]
        
        # Retrive user session
        user_session = session["user_id"]

        # Insert book into user_books table
        try:
            db.execute("INSERT INTO users_books (user_id, book_id, date_added) VALUES (?, ?, ?)", user_session, book_id, datetime.now())
        
        except:
            return apology("Book already linked to this user.")
        
        return redirect("/")
    
    else:
        # Handle search using Google Books API
        query = request.args.get("q", "").strip()

        # Check if query is empty
        if not query:
            return render_template("/add_book.html", results=None)

        query = "intitle:"+ query # use intitle in order to query the API and return books base on title name of a book

        # fetch book detials
        results = fetch_book_details(query)
        print(results)
        return render_template("/add_book.html", results=results)
    

@app.route("/book_details/<int:book_id>", methods=["GET", "POST"])
@login_required
def book_details(book_id):
    """Show details of a specif book and allow user to add personal notes."""
    
    # Retrive user session
    user_session = session["user_id"]

    if request.method == "POST":
        # check if the submitted form is for adding, remove or edit note or remove a book
        form_type = request.form.get("form_type")

        # Check if remove button has been clicked, if yes remove book from database and the notes related to it
        if form_type == "remove_book":
            db.execute("DELETE FROM users_books WHERE user_id = ? AND book_id = ?;", user_session, book_id)
            db.execute("DELETE FROM notes WHERE user_id = ? AND book_id = ?", user_session, book_id)
            return redirect("/")
        
        elif form_type == "add_note":
            # Adding of personal notes

            # Retrive note
            note = request.form.get("note", "").strip()

            if not note:
                return apology("Note cannot be empty")

            # Insert in table note
            if note:
                db.execute("INSERT INTO notes (user_id, book_id, note, date_added) VALUES (?, ?, ?, ?)", user_session, book_id, note, datetime.now())
                return redirect (f"/book_details/{book_id}")
        
        elif form_type =="remove_note":
            note_id = request.form.get("note_id")
            db.execute("DELETE FROM notes WHERE id = ? AND user_id = ? AND book_id = ?", note_id, user_session, book_id)
            return redirect (f"/book_details/{book_id}")
        
    else:
    
        # Fetch book details from the database
        book = db.execute("SELECT * FROM books WHERE id = ?", book_id)
        notes = db.execute("SELECT * FROM notes WHERE user_id = ? and book_id = ?", user_session, book_id)

        # transforming date string in actual data object so I can select the format i need in jinja
        for note in notes:
            note["date_added"] = datetime.strptime(note["date_added"], "%Y-%m-%d %H:%M:%S")

        book = book[0]

        # Fetch additional information of books from the API
        query = f"{book['title']} {book['author']}"
        additional_details = fetch_book_details(query)
        additional_details = additional_details[1]
        
        return render_template("book_details.html", book=book, additional_details=additional_details, notes=notes)
    

@app.route("/recommendation_book_detail/<book_id>", methods=["GET", "POST"])
@login_required
def recommendation_book_detail(book_id):
    
    # Make API request for the specific book base on book id
    
    book = requests.get(f"https://www.googleapis.com/books/v1/volumes/{book_id}").json()
    
    return render_template("recommendation_book_detail.html", book=book)
    


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    
    # Get the user's book from the database
    user_books = db.execute( """
                SELECT DISTINCT
                    b.title,
                    b.author, 
                    b.status,
                    CASE
                        WHEN INSTR(b.genre, '/') > 0 THEN SUBSTR(b.genre, 1, INSTR(b.genre, '/') - 2)
                        ELSE b.genre
                    END AS genre        
                FROM 
                    books AS b
                INNER JOIN 
                    users_books AS ub
                 ON b.id = ub.book_id
                WHERE
                    ub.user_id  = ?
                
                """, session["user_id"])
    
    # Convert to panda dataframe

    df = pd.DataFrame(user_books, columns=["title", "author", "status", "genre"])
    
    
    # Reccomend new books to user base on reccomandtion content system

    # Store genre and author in list 
    genres = [book["genre"]for book in user_books if book["genre"]]
    authors = [book["author"]for book in user_books if book["author"]]

    # pick up a random genre from the list, if genres empty pick it up author
    genre_or_author= ""
    if genres:
        genre_or_author = random.choice(genres)
    else:
        genre_or_author = random.choice(authors)

    # pass it as argument in the fetch book details parameter by providing keyword subject
    reccomended_books = fetch_book_details("subject:"+genre_or_author)

    # Count books by status
    status_count = {
        "To Read": sum(1 for book in user_books if book["status"] == "to_read"),
        "Currently Reading": sum(1 for book in user_books if book["status"] == "currently_reading"),
        "Read": sum(1 for book in user_books if book["status"] == "read")
    }

    # Recent books (limit to 5)
    recent_books = user_books[-3:][::-1]

    # Count books by genres
    genre_count = df["genre"].value_counts()

    # Bar Chart for count of books by genres
    
    genre_chart = go.Figure(data=[
        go.Bar(
            x=genre_count.index,                   
            y=genre_count.values,                
            marker=dict(
                color='#9B6DFF',
                line=dict(color='#E8F9FF', width=2)
                )
        )
    ])

    genre_chart.update_layout(
        title="Books per Genre",                
        xaxis_title="Genre",                     
        yaxis_title="Count",                   
        xaxis_tickangle=45,
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=40, r=40, t=50, b=50),
        paper_bgcolor="#FBFBFB",
        plot_bgcolor="#FBFBFB",
        yaxis=dict(gridcolor="#C4D9FF")
        
)


    # Bar Chart for count of books by status
    status_chart = go.Figure(data=[
        go.Bar(
            x=list(status_count.keys()),
            y=list(status_count.values()),
            text=list(status_count.values()),
            textposition="auto",
            marker=dict(
                color=['#9B6DFF', '#C4D9FF', '#7140F5', '#8A5AFF'],
                line=dict(color='#7140F5', width=1) 
                )
            )
        ])
    status_chart.update_layout(
        title="Books by Status",
        xaxis_title="Status",
        yaxis_title="Count",
        template="plotly_white",
        font=dict(family="Inter, sans-serif"),
        xaxis_tickangle=-20,
        paper_bgcolor="#FBFBFB",
        plot_bgcolor="#FBFBFB",
        yaxis=dict(gridcolor="#C4D9FF")
    )
    
    # Convert Plotly graphs to HTML
    status_chart_html = status_chart.to_html(full_html=False) # Converting in html to render in the web page
    genre_chart_html = genre_chart.to_html(full_html=False)


    return render_template("dashboard.html",
                           total_books=len(user_books),
                           status_count=status_count,
                           recent_books=recent_books,
                           status_chart=status_chart_html,
                           genre_chart=genre_chart_html,
                           reccomended_books=reccomended_books)

   



############################################################################################## Registraion, loign, log out ############################################################################


@app.route("/registration", methods=["GET", "POST"])
def registration():
    """Register user"""
    # User reached rout via POST
    if request.method == "POST":
        
        # Store user inputs inside variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validation user inputs
        if not username:
            return apology("Username field is empty.")
        
        if  db.execute("SELECT * FROM users WHERE username = ?", username):
            return apology("Username already exist")

        if not password:
            return apology("Password field is empty")
        
        if password != confirmation:
            return apology("Password does not match")
        
        # Insert data into table user
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                    username, generate_password_hash(password))
        
        # Redirect to login page
        return redirect("/login")
    
    # User reached route via GET   
    else:

         # Retrive quote from quote function
        quote = get_daily_quote()

        return render_template("registration.html", quote=quote)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in the user """

    # Forget any user_id
    session.clear()

    # User reached rout via POST 
    if request.method == "POST":
    
        # Ensure username was inserted
        if not request.form.get("username"):
            return apology("Must provide username")
        
        # Ensure password was inserted
        if not request.form.get("password"):
            return apology("Must provide password")
        
        # Query database for username
        row = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check that username exists and password is correct
        if len(row) != 1 or not check_password_hash(row[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")
        
        # Remeber which user has logged in
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET  
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
