from django.shortcuts import render
from django.template import Context

def home_page(request):
    books = [Context(dict(title=f"Book title {i}",
                          author=f"Author {i}",
                          price=0.0))
             for i in range(1, 10)]
    return render(request, "home.html", {"books": books})
