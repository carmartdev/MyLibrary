from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape, strip_tags
from django.views import generic
from django.views.decorators.http import require_POST
from store.models import Author, Book

class HomePage(generic.ListView):
    model = Book
    context_object_name = "books"
    template_name = "store/index.html"
    paginate_by = 10

    def get_queryset(self):
        self.request.session["bookmark"] = self.request.get_full_path()
        return super().get_queryset()

class Search(HomePage):
    def get_queryset(self):
        query = self.kwargs.get("query")
        query = Q(title__icontains=query) | Q(authors__name__icontains=query)
        return super().get_queryset().filter(query).distinct()

class AuthorPage(HomePage):
    def get_queryset(self):
        pk = self.kwargs.get("author_id")
        return super().get_queryset().filter(authors__key__contains=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = Author.objects.get(pk=self.kwargs.get("author_id"))
        return context


def search(request):
    query = escape(strip_tags(request.GET.get("query")))
    if query:
        return redirect("store:search-restful", query=query)
    else:
        return redirect("store:home")

class BookInfo(generic.detail.DetailView):
    model = Book
    template_name = "store/book_info.html"

@require_POST
def delete_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    cart.pop(item_id)
    request.session["cart"] = cart
    return redirect("store:cart")

@require_POST
def update_cart(request):
    cart = request.session.get("cart", {})
    qtys = dict((k, v) for k, v in request.POST.items() if k.startswith("qty"))
    for i, q in qtys.items():
        cart[i[4:]] = int(q)

    request.session["cart"] = cart
    return redirect("store:cart")

@require_POST
def add_to_cart(request, item_id):
    book = get_object_or_404(Book, pk=item_id)
    cart = request.session.get("cart", {})
    cart[book.pk] = 1
    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER"))

def show_cart(request):
    cart = request.session.get("cart", {})
    books_in_cart = Book.objects.filter(key__in=cart.keys())
    for book in books_in_cart:
        book.qty = cart[book.pk]
        book.total = book.qty * book.price
    total_price = sum(i.total for i in books_in_cart)
    return render(request, "store/cart.html",
                  {"cart": books_in_cart, "total_price": total_price})

def checkout(request):
    return render(request, "store/checkout.html")
