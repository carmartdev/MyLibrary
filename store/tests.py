from django.test import TestCase
from store.models import Book, CartItem

class HomePageTest(TestCase):
    def test_uses_index_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "store/index.html")

    def test_can_add_to_cart(self):
        response = self.client.post("/", data=dict(id="01"))


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        book1 = Book(author="Author 1", title="Book Title 1", price=0)
        book1.save()
        book2 = Book(author="Author 2", title="Book Title 2", price=0)
        book2.save()

        first_item = CartItem(book=book1)
        first_item.save()

        second_item = CartItem(book=book2)
        second_item.save()

        saved_items = CartItem.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.book_id, book1.id)
        self.assertEqual(second_saved_item.book_id, book2.id)
