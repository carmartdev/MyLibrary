from django.test import TestCase
from django.urls import reverse
from store.models import Author, Book

def create_book(key, title, price):
    book = Book(key=key, title=title, price=price)
    book.save()
    return book

def create_author(key, name):
    author = Author(key=key, name=name)
    author.save()
    return author

class HomePageTest(TestCase):
    def test_uses_index_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "store/index.html")

class CartTest(TestCase):
    def test_uses_cart_template(self):
        response = self.client.get("/cart/")
        self.assertTemplateUsed(response, "store/cart.html")

    def test_cart_page_contains_books_in_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.get(f"/cart/")
        self.assertQuerysetEqual(list(response.context["cart"]), [repr(book)])

    def test_delete_redirects_to_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post(f"/cart/item/{book.pk}/delete")
        self.assertRedirects(response, reverse("store:cart"))

    def test_can_delete_from_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post(f"/cart/item/{book.pk}/delete")
        self.assertDictEqual(self.client.session["cart"], {})

    def test_can_add_to_cart(self):
        book = create_book(key=1, title="test", price=10)
        response = self.client.post(f"/cart/item/{book.pk}/add",
                                    HTTP_REFERER="/")
        self.assertDictEqual(self.client.session["cart"], {str(book.pk): 1})

    def test_update_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post("/update", {f"qty {book.pk}": 2})
        self.assertDictEqual(self.client.session["cart"], {str(book.pk): 2})

class CheckoutTest(TestCase):
    def test_uses_checkout_template(self):
        response = self.client.get("/checkout/")
        self.assertTemplateUsed(response, "store/checkout.html")

class SearchTest(TestCase):
    def test_uses_index_template(self):
        response = self.client.get(f"/search/", {"query": "cat"}, follow=True)
        self.assertTemplateUsed(response, "store/index.html")

    def test_search_contains_books_with_keyword(self):
        book = create_book(key=1, title="Catdog", price=10)
        response = self.client.get(f"/search/", {"query": "cat"}, follow=True)
        self.assertContains(response, "Catdog")

    def test_search_not_contains_books_without_keyword(self):
        create_book(key=2, title="dog", price=10)
        response = self.client.get(f"/search/", {"query": "cat"}, follow=True)
        self.assertNotContains(response, "dog")

    def test_empty_search_redirects_to_homepage(self):
        response = self.client.get(f"/search/", {"query": ""})
        self.assertRedirects(response, reverse("store:home"))

class BookInfoTest(TestCase):
    def test_uses_book_info_template(self):
        create_book(key=1, title="test", price=10)
        response = self.client.get("/book/1/")
        self.assertTemplateUsed(response, "store/book_info.html")

class AuthorPageTest(TestCase):
    def test_uses_index_template(self):
        create_author(key=1, name="test")
        response = self.client.get("/author/1/")
        self.assertTemplateUsed(response, "store/index.html")

    def test_contains_books_by_author(self):
        author = create_author(key=1, name="Bob")
        book = Book(key=1, title="Catdog", price=10)
        book.save()
        book.authors.add(author)
        response = self.client.get(f"/author/{author.pk}/", follow=True)
        self.assertContains(response, "Catdog")

    def test_not_contains_books_by_another_author(self):
        author1 = create_author(key=1, name="Alice")
        book = Book(key=1, title="Catdog", price=10)
        book.save()
        book.authors.add(author1)
        author2 = create_author(key=2, name="Bob")
        response = self.client.get(f"/author/{author2.pk}/", follow=True)
        self.assertNotContains(response, "Catdog")
