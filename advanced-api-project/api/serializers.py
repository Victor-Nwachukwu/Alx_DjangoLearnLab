from rest_framework import serializers
from .models import Author, Book
from datetime import date

# --- 1. Book Serializer with Custom Validation ---

class BookSerializer(serializers.ModelSerializer):
    """
    SERIALIZER DOCUMENTATION: BookSerializer
    
    Purpose: Converts the Book model instance into JSON format for API responses (serialization), 
    and validates/converts incoming data from clients for creating/updating Books (deserialization).
    
    Relationship Handling (Input):
    When creating or updating a book, the 'author' field expects the primary key (ID) of an existing Author.
    This is the default handling for a ForeignKey field in a ModelSerializer.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        CUSTOM VALIDATION: publication_year
        
        Ensures the entered publication year is not a date in the future and is 
        set to a realistic historical year (post-Gutenberg).
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. The current year is {current_year}."
            )
        # Setting an arbitrary but reasonable historical cut-off
        if value < 1450:
             raise serializers.ValidationError(
                "Publication year must be 1450 or later, reflecting the era of modern printing."
            )
            
        return value

# --- 2. Author Serializer with Nested Book Serialization ---

class AuthorSerializer(serializers.ModelSerializer):
    """
    SERIALIZER DOCUMENTATION: AuthorSerializer
    
    Purpose: Converts the Author model instance into a comprehensive JSON format, 
    including all related books.
    
    Relationship Handling (Output/Nested Serialization):
    The Author model is linked to many Books (One-to-Many relationship).
    We use nested serialization to fetch and display the related Books directly 
    within the Author's JSON representation. 
    """
    
    # NESTED FIELD: 
    # The field name 'books' must match the 'related_name' specified on the 
    # ForeignKey field in the Book model (Book.author).
    # - `BookSerializer(many=True)`: Indicates we expect a list of Book objects.
    # - `read_only=True`: Ensures this field is only used for output/display (GET requests) 
    #   and cannot be used to modify related books through the Author endpoint.
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] # 'books' is the custom field including nested data