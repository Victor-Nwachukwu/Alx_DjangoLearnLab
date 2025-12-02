from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics, mixins, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework  
class AuthorViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Author.
    The AuthorSerializer includes nested books (read-only).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Book.
    BookSerializer enforces publication_year validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    
    Advanced querying capabilities:
    - Filtering by fields: title, author, publication_year
      Example: /api/books/?author=1&publication_year=2020
    - Searching by text in title or author's name
      Example: /api/books/?search=harry
    - Ordering results by fields (title, publication_year)
      Example: /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Backends for filtering, search, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields allowed for filtering via query params
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields used for search via ?search=term
    search_fields = ['title', 'author__name']

    # Fields allowed for ordering via ?ordering=field
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/
    - Retrieve a single Book by primary key.
    - Read-only for unauthenticated users.
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/
    - Create a new Book.
    - Restricted to authenticated users.
    - Uses serializer validation for publication_year (already implemented in serializer).
    - Example customization points:
       * override perform_create() to attach metadata or transform input
       * override create() to change response format or status codes
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can create

    def perform_create(self, serializer):
        """
        Called after serializer.is_valid() and before saving the instance.
        Use this to add or modify data not supplied by the client.
        Example: set a created_by field (if you had one), or perform logging.
        We're not modifying the Book fields here because Book.author should be supplied
        by the client (per your model), but this is where you'd set defaults if needed.
        """
        # e.g. serializer.save(created_by=self.request.user)
        serializer.save()


    def create(self, request, *args, **kwargs):
        """
        Explicitly call serializer.is_valid(raise_exception=True) to ensure
        validation errors return with standard DRF error responses.
        Then return the created object with a 201 status.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   # will return 400 with error details
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<pk>/
    - Update an existing Book instance.
    - Restricted to authenticated users (you might narrow this to owners/admins).
    - Validates input using serializer's validation logic.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # change to custom owner-only permission if needed

    def perform_update(self, serializer):
        """
        Place to perform extra logic before saving updates (e.g., audit trails).
        """
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Ensure partial and full updates both validate and use DRF's standard responses.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/
    - Deletes a book.
    - Highly sensitive: restrict to admins by default.
    - If you prefer to let authors delete their books, create a custom permission.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]  # only admin users can delete by default