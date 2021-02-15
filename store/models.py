from django.db import models

class Author(models.Model):
    key = models.CharField(max_length=10, primary_key=True)
    name = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Book(models.Model):
    key = models.CharField(max_length=11, primary_key=True)
    title = models.TextField()
    authors = models.ManyToManyField(Author)
    publisher = models.TextField()
    publish_date = models.CharField(max_length=50)
    description = models.TextField()
    cover = models.CharField(max_length=7)
    isbn_10 = models.CharField(max_length=10)
    isbn_13 = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("store:book", args=[self.id])
