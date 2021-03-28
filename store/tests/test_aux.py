from django.test import TestCase
from store.templatetags.aux import extract_keywords

class AuxTest(TestCase):
    def test_uses_index_template(self):
        uri = "http://localhost:8000/search/cat%20and%20dog/"
        self.assertEqual(extract_keywords(uri), "cat and dog")
