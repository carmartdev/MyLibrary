from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    price = models.IntegerField()


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
