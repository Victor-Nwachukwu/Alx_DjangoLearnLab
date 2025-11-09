📚 Django ORM CRUD Operations — Book Model

This document demonstrates the use of Django’s Object-Relational Mapper (ORM) to perform Create, Retrieve, Update, and Delete (CRUD) operations on the Book model within the bookshelf app.

🧩 Model Definition

# bookshelf/models.py

from django.db import models

class Book(models.Model):
title = models.CharField(max_length=200)
author = models.CharField(max_length=100)
publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

⚙️ Setup and Migration

Before performing CRUD operations, ensure the app and model are set up and migrated:

python manage.py makemigrations bookshelf
python manage.py migrate

✅ These commands create the database table for the Book model.

📘 CREATE OPERATION

Objective: Create a Book instance with the title “1984”, author “George Orwell”, and publication year 1949.

from bookshelf.models import Book

# Create a new book record

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Verify creation

book

Expected Output:

# <Book: 1984 by George Orwell (1949)>

# The book has been successfully created and saved in the database.

📗 RETRIEVE OPERATION

Objective: Retrieve and display all attributes of the created book.

from bookshelf.models import Book

# Retrieve the book by its title

book = Book.objects.get(title="1984")

# Display the book details

print(book.title, book.author, book.publication_year)

Expected Output:

# 1984 George Orwell 1949

# The book details were successfully retrieved from the database.

📙 UPDATE OPERATION

Objective: Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.

from bookshelf.models import Book

# Get the book to update

book = Book.objects.get(title="1984")

# Update the title

book.title = "Nineteen Eighty-Four"
book.save()

# Confirm update

print(book.title)

Expected Output:

# Nineteen Eighty-Four

# The book title has been successfully updated.

📕 DELETE OPERATION

Objective: Delete the updated book and confirm the deletion.

from bookshelf.models import Book

# Get the book to delete

book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book

book.delete()

# Confirm deletion

Book.objects.all()

Expected Output:

# <QuerySet []>

# The book has been successfully deleted from the database.
