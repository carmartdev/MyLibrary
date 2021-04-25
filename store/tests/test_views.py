import json
from django.test import TestCase
from django.urls import reverse
from store.models import Author, Book
from store.serializers import BookSerializer

def create_book(key, title, price):
    book = Book(key=key, title=title, price=price)
    book.save()
    return book

def create_author(key, name):
    author = Author(key=key, name=name)
    author.save()
    return author

class BookViewSetTest(TestCase):
    def test_root_url_redirects_to_book_list(self):
        response = self.client.get("/")
        self.assertRedirects(response, reverse("store:book-list"))

    def test_get_returns_json_200(self):
        response = self.client.get("/", follow=True,
                                   HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_search_uses_index_template(self):
        response = self.client.get("/", {"search": "cat"}, follow=True)
        self.assertTemplateUsed(response, "store/index.html")

    def test_search_contains_books_with_keyword(self):
        book = create_book(key=1, title="Catdog", price=10)
        response = self.client.get("/", {"search": "cat"}, follow=True)
        self.assertContains(response, "Catdog")

    def test_search_not_contains_books_without_keyword(self):
        create_book(key=2, title="dog", price=10)
        response = self.client.get("/", {"search": "cat"}, follow=True)
        self.assertNotContains(response, "dog")

    def test_empty_search_redirects_to_book_list(self):
        response = self.client.get("/", {"search": ""})
        self.assertRedirects(response, reverse("store:book-list"))

    def test_book_details_page_uses_book_details_template(self):
        create_book(key=1, title="test", price=10)
        response = self.client.get(f"{reverse('store:book-list')}1/")
        self.assertTemplateUsed(response, "store/book_details.html")

    def test_author_page_uses_index_template(self):
        author = create_author(key=1, name="test")
        response = self.client.get(
            f"{reverse('store:book-list')}?author={author.pk}")
        self.assertTemplateUsed(response, "store/index.html")

    def test_author_page_contains_books_by_author(self):
        author = create_author(key=1, name="Bob")
        book = Book(key=1, title="Catdog", price=10)
        book.save()
        book.authors.add(author)
        response = self.client.get(
            f"{reverse('store:book-list')}?author={author.pk}", follow=True)
        self.assertContains(response, "Catdog")

    def test_author_page_not_contains_books_by_another_author(self):
        author1 = create_author(key=1, name="Alice")
        book = Book(key=1, title="Catdog", price=10)
        book.save()
        book.authors.add(author1)
        author2 = create_author(key=2, name="Bob")
        response = self.client.get(
            f"{reverse('store:book-list')}?author={author2.pk}", follow=True)
        self.assertNotContains(response, "Catdog")

class CartTest(TestCase):
    def test_uses_cart_template(self):
        response = self.client.get(reverse("store:cart"))
        self.assertTemplateUsed(response, "store/cart.html")

    def test_get_returns_json_200(self):
        response = self.client.get(reverse("store:cart"),
                                   HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_cart_page_contains_books_in_cart_html(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        qty = 2
        session["cart"] = {book.pk: qty}
        session.save()
        response = self.client.get(reverse("store:cart"))
        self.assertListEqual(response.context["cart"],
                             [dict(qty=qty,
                                   total=book.price * qty,
                                   **BookSerializer(book).data)])

    def test_cart_page_contains_books_in_cart_json(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        qty = 5
        session["cart"] = {book.pk: qty}
        session.save()
        response = self.client.get(reverse("store:cart"),
                                   HTTP_ACCEPT="application/json")
        self.assertListEqual(json.loads(response.content.decode())["cart"],
                             [dict(qty=qty,
                                   total=f"{book.price * qty:.2f}",
                                   **BookSerializer(book).data)])

    def test_delete_redirects_to_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post(reverse("store:cart-delete"),
                                    {"book_id": book.pk},
                                    HTTP_ACCEPT="text/html")
        self.assertRedirects(response, reverse("store:cart"))

    def test_delete_from_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post(reverse("store:cart-delete"),
                                    {"book_id": book.pk},
                                    HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(self.client.session["cart"], {})

    def test_add_to_cart(self):
        book = create_book(key=1, title="test", price=10)
        response = self.client.post(reverse("store:cart-add"),
                                    {"book_id": book.pk},
                                    HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(self.client.session["cart"], {str(book.pk): 1})

    def test_add_redirects_to_referrer(self):
        book = create_book(key=1, title="test", price=10)
        response = self.client.post(reverse("store:cart-add"),
                                    {"book_id": book.pk},
                                    HTTP_REFERER=reverse("store:book-list"),
                                    HTTP_ACCEPT="text/html")
        self.assertRedirects(response, reverse("store:book-list"))

    def test_update_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post(reverse("store:cart-update"),
                                    {f"qty {book.pk}": 2},
                                    HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(self.client.session["cart"], {str(book.pk): 2})

    def test_update_redirects_to_cart(self):
        book = create_book(key=1, title="test", price=10)
        session = self.client.session
        session["cart"] = {book.pk: 1}
        session.save()
        response = self.client.post(reverse("store:cart-update"),
                                    {f"qty {book.pk}": 2},
                                    HTTP_ACCEPT="text/html")
        self.assertRedirects(response, reverse("store:cart"))

class CheckoutTest(TestCase):
    def test_uses_checkout_template(self):
        response = self.client.get(reverse("store:checkout"))
        self.assertTemplateUsed(response, "store/checkout.html")
