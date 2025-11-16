from bookshelf.models import Book

# Get the book to delete

book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book

book.delete()

# Confirm deletion

Book.objects.all()

# Output: <QuerySet []> # confirms deletion
