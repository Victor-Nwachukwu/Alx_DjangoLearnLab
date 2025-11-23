from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    It handles converting Book instances to native Python datatypes 
    that can be rendered into JSON/XML, and handles deserialization
    back into Python datatypes before saving to the model.
    """
    class Meta:
        # 1. Specify the model to use
        model = Book
        
        # 2. Specify all fields from the model to be included in the API response
        # Using '__all__' is convenient for simple models.
        fields = '__all__'
        
        # If you wanted to list them explicitly:
        # fields = ['id', 'title', 'author', 'created_at']