# relationship_app/query_samples.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"No author named '{author_name}'")
        return []

    books = Book.objects.filter(author=author) 
    for book in books:
        print("-", book.title)
    return list(books)

def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library named '{library_name}'")
        return []

    books = library.books.all()
    print(f"Books in {library_name}:")
    for book in books:
        print("-", book.title)
    return list(books)

def librarian_for_library(library_name):
    from relationship_app.models import Library, Librarian

    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library named '{library_name}'")
        return None

    try:
        librarian = Librarian.objects.get(library=library)  
        print(f"Librarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian set for {library_name}")
        librarian = None

    return librarian