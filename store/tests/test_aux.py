from django.test import TestCase
from store.templatetags.aux import extract_keywords, names

class AuxTest(TestCase):
    def test_extract_keywords(self):
        uri = "http://localhost:8000/books/?search=cat%20and%20dog"
        self.assertEqual(extract_keywords(uri), "cat and dog")

    def test_names(self):
        nlist = [{"name": name} for name in ("Alice", "Bob")]
        self.assertEqual(names(nlist),"Alice, Bob")
