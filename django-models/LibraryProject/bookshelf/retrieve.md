from bookshelf.models import Book

# Retrieve the book by its title

book = Book.objects.get(title="1984")

# Display the book details

print(book.title, book.author, book.publication_year)

# Output: 1984 George Orwell 1949
