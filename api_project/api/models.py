# api/models.py

from django.db import models

class Book(models.Model):
    """
    A simple model representing a book, designed for use in the first API.
    """
    title = models.CharField(max_length=255, help_text="The title of the book.")
    author = models.CharField(max_length=150, help_text="The author of the book.")
    
    # Optional field to track creation time, good practice for APIs
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders books by title alphabetically by default
        ordering = ['title'] 

    def __str__(self):
        """
        String representation of the Book object (used in the admin and shell).
        """
        return f"{self.title} by {self.author}"