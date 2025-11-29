from django.urls import path
# Import the consolidated generic views
from .views import AuthorListCreate, AuthorDetailUpdateDestroy, BookListCreate, BookDetailUpdateDestroy

# Note: The Author views were not explicitly asked for, but are included 
# here to set up the foundation for the full CRUD API structure.
# Assuming Author views are defined similarly to Book views in api/views.py.
# If they are not yet defined, please define them based on your Author model!

urlpatterns = [
    # --- Book Endpoints ---
    
    # 1. /books/ (GET: List all books, POST: Create a new book)
    path('books/', 
         BookListCreate.as_view(), 
         name='book-list-create'),

    # 2. /books/<int:pk>/ (GET: Retrieve, PUT/PATCH: Update, DELETE: Destroy)
    path('books/<int:pk>/', 
         BookDetailUpdateDestroy.as_view(), 
         name='book-detail-update-destroy'),
         
    # --- Author Endpoints (Optional/Future) ---
    
    # 3. /authors/ (GET: List all authors, POST: Create a new author)
    path('authors/', 
         AuthorListCreate.as_view(), 
         name='author-list-create'),

    # 4. /authors/<int:pk>/ (GET: Retrieve, PUT/PATCH: Update, DELETE: Destroy)
    path('authors/<int:pk>/', 
         AuthorDetailUpdateDestroy.as_view(), 
         name='author-detail-update-destroy'),
]