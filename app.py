###### MAKE IT in a way that when select a book it open a page with specifc details about the book
### and personal detail the user can add on that page like favourites quotes etc.

# check why when I check arry potter it does not geve e useful answert but random books from random authors


# To update requirments.txt with latest packages  :::   pip freeze > requirements.txt
# citie the usage of CS50x code for thing like caching, sessions, apology etc (refere to the base implemnetation of finance assignment) maybe change the code logic to show my understiandg and modificaiton
# make from scratch the layout.html page (it is fully copy from cs50x so make it from scratch)
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

from helpers import login_required, apology

# Google books API
KEY = "AIzaSyDx2n2KoQeViQl3jY0XtTde1BnGPDg5nzg"

# Configure application 
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")

#TODO probably when web application going in production the cache has to come back (?)
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
                    b.title,
                    b.author, 
                    b.status 
                FROM 
                    books AS b
                INNER JOIN 
                    users_books AS ub
                 ON b.id = ub.book_id
                WHERE
                    ub.user_id  = ?
                
                """, session["user_id"]
            )
        
        return render_template("index.html", user_books=user_books)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    """ User can search and add a book. """

    if request.method == "POST":
        
        # Store input inside variables
        book_title = request.form.get("book_title")
        author = request.form.get("author")
        status = request.form.get("status")
        
        # Validate user input
        if not book_title or not author or not status:
            return apology("All fields are required!")
        
        # Check if book already exists in the database
        book = db.execute("SELECT * FROM books WHERE title = ? AND author = ?", book_title, author)
        if not book:
            
            # Insert book into table if does not exists
            book_id = db.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", book_title, author, status)
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
        query = request.args.get("q")
        results = []

        if query:
            # Make API request

            api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=en&maxResults=5&key={KEY}"
            response = requests.get(api_url).json()

            if "items" in response:
                for item in response["items"]:
                    book_info = item["volumeInfo"]
                    results.append({
                        "title": book_info.get("title"),
                        "author": ", ".join(book_info.get("authors", [])),
                        "image": book_info.get("imageLinks", {}).get("thumbnail", ""),
                        "id": item.get("id")
                    })

        return render_template("/add_book.html", results=results)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

#TODO make visually these data (plotly)
#TODO adding book reccomantion based on user books collection
    
    # Get the user's book from the database
    user_books = db.execute( """
                SELECT DISTINCT
                    b.title,
                    b.author, 
                    b.status 
                FROM 
                    books AS b
                INNER JOIN 
                    users_books AS ub
                 ON b.id = ub.book_id
                WHERE
                    ub.user_id  = ?
                
                """, session["user_id"])

    # Count books by status
    status_count = {
        "To Read": sum(1 for book in user_books if book["status"] == "to_read"),
        "Currently Reading": sum(1 for book in user_books if book["status"] == "currently_reading"),
        "Read": sum(1 for book in user_books if book["status"] == "read")
    }

    # Recent books (limit to 5)
    recent_books = user_books[-5:][::-1]

    return render_template("dashboard.html",
                           total_books=len(user_books),
                           status_count=status_count,
                           recent_books=recent_books)

    
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
        return render_template("registration.html")


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
