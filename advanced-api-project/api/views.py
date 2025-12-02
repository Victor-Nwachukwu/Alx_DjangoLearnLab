from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# You will need to install 'django-filter' and add 'django_filters' to INSTALLED_APPS
# pip install django-filter

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# --- Author Views ---

class AuthorListCreate(ListCreateAPIView):
    """
    Handles: GET /authors/ (List) and POST /authors/ (Create)
    Permissions: Read for all, Write (POST) for authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Customization: Allows ordering authors by name
    filter_backends = [OrderingFilter]
    ordering_fields = ['name']


class AuthorDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Handles: GET /authors/<int:pk>/ (Retrieve), PUT/PATCH (Update), DELETE (Destroy)
    Permissions: Read for all, Write (MUTATIONS) for authenticated users.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# --- Book Views with Advanced Querying (Filtering, Search, Ordering) ---

class BookListCreate(ListCreateAPIView):
    """
    Handles: GET /books/ (List) and POST /books/ (Create)
    
    This view implements advanced query features:
    1. Filtering: By author ID, publication year, and title.
    2. Searching: By book title and author name.
    3. Ordering: By publication year and title.
    
    Permissions: Read access for all, Write access for authenticated users.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    
    # Permissions: Read for all, Write (POST) for authenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configuration for Filtering, Searching, and Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Step 1: Filtering Configuration (DjangoFilterBackend)
    # Allows filtering by exact matches on these fields:
    # Example: /books/?publication_year=2000&author=1
    filterset_fields = ['author', 'publication_year', 'title'] 

    # Step 2: Search Configuration (SearchFilter)
    # Allows full-text search across these fields using the 'search' parameter:
    # Example: /books/?search=Tolkien
    # To search the Author's name, use the ForeignKey relationship syntax: author__name
    search_fields = ['title', 'author__name']

    # Step 3: Ordering Configuration (OrderingFilter)
    # Allows sorting the results using the 'ordering' parameter:
    # Example: /books/?ordering=-publication_year,title
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title'] # Default ordering if none is provided


class BookDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Handles: GET /books/<int:pk>/ (Retrieve), PUT/PATCH (Update), DELETE (Destroy)
    Permissions: Read for all, Write (MUTATIONS) for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]