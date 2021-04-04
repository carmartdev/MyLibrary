from django.test import TestCase
from store.models import Author, Book

class AuthorModelTest(TestCase):
    def test_get_absolute_url(self):
        author = Author(key=1, name="Bob")
        self.assertEqual(author.get_absolute_url(),
                         f"/books/?author={author.pk}")

    def test_string_representation(self):
        author = Author(key=1, name="Bob")
        self.assertEqual(str(author), "Bob")

class BookModelTest(TestCase):
    def test_get_absolute_url(self):
        book = Book(key=1, title="Catdog", price=10)
        self.assertEqual(book.get_absolute_url(), f"/books/{book.pk}/")

    def test_string_representation(self):
        author1 = Author(key=1, name="Alice")
        author1.save()
        author2 = Author(key=2, name="Bob")
        author2.save()
        book = Book(key=1, title="Catdog", price=10)
        book.save()
        book.authors.add(author1, author2)
        self.assertEqual(str(book), "Catdog by Alice, Bob")
