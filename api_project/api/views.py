from rest_framework import viewsets
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    
class BookViewSet (viewsets.ModelViewSet):
    """
    A ViewSet that automatically provides 'list', 'create', 'retrieve', 
    'update', and 'destroy' actions for the Book model.
    
    This consolidates all standard CRUD logic into a single class.
    """
    
    # 1. Define the queryset: The base set of objects the view will operate on.
    queryset = Book.objects.all().order_by('title')
    
    # 2. Define the serializer_class: The serializer used for both input validation 
    # (CREATE, UPDATE) and output formatting (LIST, RETRIEVE).
    serializer_class = BookSerializer

# We are replacing the previous BookList view with this comprehensive BookViewSet.
# This means we will also need to update api/urls.py to use a Router 
# instead of manual path() definitions to leverage the full ViewSet functionality.