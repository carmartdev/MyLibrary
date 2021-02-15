from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "publish_date", "description",
                    "cover", "isbn_10", "isbn_13", "price",)
    filter_horizontal = ("authors",)

admin.site.register(Book, BookAdmin)
