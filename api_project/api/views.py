from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all Book objects.
    
    This view handles GET requests, retrieves all instances of the Book model,
    and returns them as a JSON array using the BookSerializer.
    """
    
    # 1. Define the queryset: Which records should this view operate on?
    # In this case, we want all books.
    queryset = Book.objects.all()
    
    # 2. Define the serializer_class: How should the data be structured (JSON)?
    serializer_class = BookSerializer

# Note: ListAPIView is read-only and automatically handles pagination and filtering 
# if you configure them later.