# Your BookshelfSpace
### Video Demo: [Click here to watch the video](https://www.youtube.com/watch?v=TtKnFycGcK8)


### Description of the project
#### Introduction:
I have developed a web application that allows users to create a personal bookshelf where they can add books they want to read, are currently reading, or plan to read in the future. The application is designed to be minimal, with the goal of not overwhelming the user and focusing on core functionalities.

#### Technologies used:
The technologies that has been user are:
- Python
- Flask
- SQL
- HTML, CSS and Javascript

#### Features:
The user can search for a book in a search bar, see a list of books, and select the desired book while choosing its status (to read, currently reading, read). The Google Books API has been used. The selected book will then be stored in a table on the home page, displaying the title, author, status, and the date it was added. The user can click on the title to open a new page showing the book’s details. On this page, the user can add and remove notes about the book, as well as remove the book from the bookshelf.

In the Overview page, a dashboard provides different metrics to give the user a quick glance at their bookshelf. These metrics include the total number of books in the library, the most recently added book, a graph showing the distribution of books by status (to read, currently reading, read), and another graph displaying books per genre. The Pandas library has been used to create these charts.

Additionally, the Overview page includes a list of recommended books based on the user's genre preferences. The user can add these recommended books to their bookshelf. This phase was particularly interesting because I initially thought that implementing a recommendation system would require writing a complex algorithm. However, I realized that I could simply use the function I had already created to fetch books from the Google Books API. Instead of passing a book title, I only needed to pass a randomly selected genre from those present in the user’s bookshelf. This insight was valuable to me—it showed that sometimes, what seems complex to implement may actually have a simple solution.

The registration and login pages have also been implemented. On the registration page, a quote is fetched and displayed.

#### Database structure:
- Books
- Notes
- users
- users_book
#### Files:
- app.py: manages the logic of the web application
- helpers.py: functions used in the main logic (api call function, daily quote, ) 
-db_structure_setup.py: the script to realize the database tables
- templates: all the html pages
- static: the css file
