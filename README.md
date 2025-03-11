# Your BookshelfSpace


# 📚 Your BookshelfSpace  

## 📌 Project Overview  
**Your BookshelfSpace** is a minimalistic web application that allows users to manage their personal bookshelf. Users can add books they want to read, are currently reading, or have already read. The goal of this project is to provide a simple and distraction-free experience while offering useful features to track reading progress.  

## 🛠 Technologies Used  
This project is built using the following technologies:  
- **Python** (Backend)  
- **Flask** (Web framework)  
- **SQL** (Database management)  
- **HTML, CSS, and JavaScript** (Frontend)  

## 🚀 Features  

### 📖 Book Management  
✔️ Search for books using a **search bar** powered by the **Google Books API**.  
✔️ Add books to your personal bookshelf, categorizing them as:  
   - 📍 **To Read**  
   - 📖 **Currently Reading**  
   - ✅ **Read**  
✔️ Books are stored in a table on the home page, displaying:  
   - **Title**  
   - **Author**  
   - **Status**  
   - **Date Added**  
✔️ Click on a book title to view **detailed information**, where users can:  
   - 📝 **Add and remove personal notes** about the book.  
   - ❌ **Remove books** from the bookshelf.  

### 📊 Overview Dashboard  
✔️ A **dashboard** provides insights into the user’s reading habits, displaying:  
   - 📚 **Total books in the library**  
   - 🔍 **Most recently added book**  
   - 📊 **A pie chart** showing the distribution of books by status (**To Read, Currently Reading, Read**)  
   - 📖 **A bar chart** displaying the number of books per genre  
✔️ The **Pandas** library is used for data processing and visualization.  

### 🤖 Book Recommendations  
✔️ The **Overview** page suggests books based on the user’s **preferred genres**.  
✔️ Instead of implementing a complex recommendation algorithm, the system intelligently selects a **random genre** from the user's existing books and fetches **new recommendations** from the **Google Books API**.  

### 🔑 User Authentication  
✔️ **Registration and login functionality** for personalized book tracking.  
✔️ The **registration page** displays a **daily motivational quote**, retrieved from an external API.  

## 🗄 Database Structure  
The project uses a relational database with the following tables:  

| Table Name  | Description |
|-------------|------------|
| `books`      | Stores book information. |
| `notes`      | Contains user-added notes. |
| `users`      | Stores user authentication details. |
| `users_book` | Tracks which books belong to which user. |

---

## 🎥 Video Demo  
[![Watch the video](https://img.youtube.com/vi/TtKnFycGcK8/0.jpg)](https://www.youtube.com/watch?v=TtKnFycGcK8)  


✅ **This project was developed as my final project for Harvard’s CS50x (Introduction to Computer Science).**  

