from cs50 import SQL
from datetime import datetime, timedelta
from flask import redirect, render_template, session
from functools import wraps
import requests
import random


# Global varable to store quote and last fetch time

cached_quote = {"quote":None, "author":None, "last_fetched": None}

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")

# Google books API
KEY = "YOUR_API_KEY_HERE"


def fetch_book_details(query):
    """Fetch book details, return list of book details if found, or an empty list if no result found"""


    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=en&maxResults=4&printType=books&orderBy=relevance&key={KEY}"

    try:
        # Make API request
        response = requests.get(api_url).json()
        books = []
        
        if "items" in response:
            for item in response["items"]:
                books.append({
                    "id": item.get("id"),
                    "selfLink": item.get("selfLink")
                })
                book_info = item["volumeInfo"]
                if book_info.get("language") == "en": # Include only book in English
                    books.append({
                        "title": book_info.get("title"),
                        "author": ", ".join(book_info.get("authors", [])),
                        "genres": ", ".join(book_info.get("categories", [])),
                        "imglarge": book_info.get("imageLinks", {}).get("large", ""),
                        "image": book_info.get("imageLinks", {}).get("thumbnail", ""),
                        "description": book_info.get("description"),
                        "id": item.get("id"),
                        "avgrating": book_info.get("averageRating")
                        })
            return books
        else:
            return []
        
    except Exception as e:
        # Handle errors like API failure, no internet connection etc
        print(f"Error fetching books details: {e}")
        return []
    

def get_daily_quote():
    """ Fetch a quote from the zenquotes API at interval of 1 minute time. Return fetched quote """
    global cached_quote

    # define the current time and interval
    interval = timedelta(minutes=1)
    now = datetime.now()

    # Check if quote, time exists and was fetched within the interval
    if cached_quote["quote"] and cached_quote["last_fetched"] and now - cached_quote["last_fetched"] < interval:
        return cached_quote
    
    # if not Fetch quote with api call and stored in cached_quote variable
    try:
        response = requests.get("https://zenquotes.io/api/quotes").json()

        if response:
            random_quote = random.choice(response)
            cached_quote = {
                "quote": random_quote["q"],
                "author": random_quote["a"],
                "last_fetched": now
            }
        else:
            cached_quote = {
                "quote": "No available quote at the moment.",
                "author": "Unknown",
                "last_fetched": now
            }

    except Exception as e :
     # Handle errors like API failure, no internet connection etc
        print(f"Error fetching books details: {e}")
    
    return cached_quote



    

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
