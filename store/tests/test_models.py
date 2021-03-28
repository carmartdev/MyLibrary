from django.test import TestCase
from store.models import Author, Book

class AuthorModelTest(TestCase):
    def test_get_absolute_url(self):
        author = Author(key=1, name="Bob")
        self.assertEqual(author.get_absolute_url(), f"/author/{author.pk}/")

class BookModelTest(TestCase):
    def test_get_absolute_url(self):
        book = Book(key=1, title="Catdog", price=10)
        self.assertEqual(book.get_absolute_url(), f"/book/{book.pk}/")
