from django.urls import path
from .views import BookList

urlpatterns = [
    # Maps the root path of the app (e.g., /api/books/) to the BookList view
    path('books/', BookList.as_view(), name='book-list'),
]