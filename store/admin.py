from django.contrib import admin
from .models import Author, Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Key", {"fields": ["key"], "classes": ["collapse"]}),
        ("Book details", {"fields": ("title", "authors", "description",
                                     "cover")}),
        ("Price", {"fields": ["price"]}),
        ("Publish information", {"fields": ("publisher", "publish_date")}),
        ("ISBN", {"fields": ("isbn_10", "isbn_13")}),
    )
    list_display = ("title", "_authors", "publish_date", "isbn_10", "isbn_13",
                    "price",)
    filter_horizontal = ("authors",)
    search_fields = ("title", "authors__name", "publish_date", "isbn_10",
                     "isbn_13", "price",)

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
