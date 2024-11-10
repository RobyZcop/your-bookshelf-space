# To update requirments.txt with latest packages  :::   pip freeze > requirements.txt
# citie the usage of CS50x code for thing like caching, sessions, apology etc (refere to the base implemnetation of finance assignment) maybe change the code logic to show my understiandg and modificaiton
# make from scratch the layout.html page (it is fully copy from cs50x so make it from scratch)
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":

        user_books = db.execute(
            "SELECT title, author, status FROM books;"
        )

        books = [{"title": book["title"], "author": book["author"], "status": book["status"]} for book in user_books]

        print(books)
        return render_template("index.html", books=books)

@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    """ User can add a book. """

    if request.method == "POST":
        
        # Store input inside variables
        book_title = request.form.get("book_title")
        author = request.form.get("author")
        status = request.form.get("status")
        
        # Validate user input
        if not book_title:
            return apology("Insert book title!")
        
        if not author:
            return apology("Insert author!")
        
        if not status:
            return apology("insert status")
        
        # Insert data into book table
        db.execute("INSERT INTO books (title, author, status) VALUES (?,?,?)",
                    book_title, author, status)
        
        flash("Book has been added successfully!")
        return redirect("/")
        
       
    else:
         return render_template("/add_book.html")

    
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

    
  