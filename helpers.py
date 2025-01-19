# mention the usage of function created already by cs50x apology and login required maybe change the logic and code

from flask import redirect, render_template, session
from functools import wraps
import requests

# Google books API
KEY = "AIzaSyDx2n2KoQeViQl3jY0XtTde1BnGPDg5nzg"


def fetch_book_details(query):
    """Fetch book details, return list of book details if found, or an empty list if no result found"""

    api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query}&langRestrict=en&maxResults=10&printType=books&orderBy=relevance&key={KEY}"

    try:
        # Make API request
        response = requests.get(api_url).json()
        books = []
        
        if "items" in response:
            for item in response["items"]:
                book_info = item["volumeInfo"]
                if book_info.get("language") == "en": # Include only book in English 
                    books.append({
                        "title": book_info.get("title"),
                        "author": ", ".join(book_info.get("authors", [])),
                        "image": book_info.get("imageLinks", {}).get("thumbnail", ""),
                        "description": book_info.get("description"),
                        "id": item.get("id")
                        })
            return books
        else:
            return []
        
    except Exception as e:
        # Handle errors like API failure, no internet connection etc
        print(f"Error fetching books details: {e}")
        return []
    

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