from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up test users, authors, and books.
        """
        # Create users
        self.user = User.objects.create_user(username='user1', password='password123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books
        self.book1 = Book.objects.create(title="Book One", publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2021, author=self.author2)

    # -----------------------------------
    # Test CRUD endpoints
    # -----------------------------------

    def test_list_books_public(self):
        """
        Anyone can list books.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_public(self):
        """
        Anyone can retrieve book details.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        """
        Authenticated users can create books.
        """
        self.client.login(username='user1', password='password123')
        url = reverse('book-create')
        data = {'title': 'Book Three', 'publication_year': 2022, 'author': self.author1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='Book Three').author, self.author1)

    def test_create_book_unauthenticated(self):
        """
        Unauthenticated users cannot create books.
        """
        url = reverse('book-create')
        data = {'title': 'Book Three', 'publication_year': 2022, 'author': self.author1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_book_authenticated(self):
        """
        Authenticated users can update books.
        """
        self.client.login(username='user1', password='password123')
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Book One', 'publication_year': 2020, 'author': self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')

    def test_delete_book_admin_only(self):
        """
        Only admin can delete books.
        """
        # Try as regular user
        self.client.login(username='user1', password='password123')
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Try as admin
        self.client.login(username='admin', password='admin123')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.filter(id=self.book1.id).count(), 0)

    # -----------------------------------
    # Test filtering, searching, ordering
    # -----------------------------------

    def test_filter_books_by_author(self):
        url = reverse('book-list') + f'?author={self.author1.id}'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)

    def test_search_books_by_title(self):
        url = reverse('book-list') + '?search=Two'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_order_books_by_publication_year(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))