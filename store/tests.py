from django.test import TestCase
from store.models import Book

class HomePageTest(TestCase):
    def test_uses_index_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "store/index.html")

    def test_can_add_to_cart(self):
        response = self.client.post("/", data=dict(id="01"))
