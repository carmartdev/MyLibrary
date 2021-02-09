from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
