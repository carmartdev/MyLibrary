from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ["key", "name"]

class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ["key", "title", "authors", "publisher", "publish_date",
                  "description", "cover", "isbn_10", "isbn_13", "price"]
