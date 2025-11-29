from django.db import models

class Author(models.Model):
    """
    MODEL DOCUMENTATION: Author
    
    Purpose: Stores information about a book's author. This is the "One" side 
    of the One-to-Many relationship with the Book model.
    """
    name = models.CharField(
        max_length=150, 
        unique=True, 
        help_text="The full name of the author."
    )

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    MODEL DOCUMENTATION: Book
    
    Purpose: Represents a single published book. This is the "Many" side 
    of the One-to-Many relationship, where multiple books link back to one Author.
    """
    title = models.CharField(
        max_length=255, 
        help_text="The main title of the book."
    )
    
    publication_year = models.IntegerField(
        help_text="The year the book was published."
    )
    
    # RELATIONSHIP HANDLING:
    # Foreign Key linking to the Author model.
    # - on_delete=models.CASCADE: If the related Author is deleted, all their 
    #   associated Books are automatically deleted.
    # - related_name='books': This crucial setting allows us to access all 
    #   books belonging to an author using the query: `author_instance.books.all()`. 
    #   This 'books' name is used in the nested serializer.
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books', 
        help_text="The author of this book."
    )

    class Meta:
        unique_together = ('title', 'publication_year')
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author.name}"