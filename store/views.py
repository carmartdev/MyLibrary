from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import filters, viewsets
from store.models import Book
from store.serializers import BookSerializer

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "authors__name"]

    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get("author", None)
        if author_id:
            queryset = queryset.filter(authors__key__contains=author_id)
        return queryset

    def list(self, request, *args, **kwargs):
        self.request.session["bookmark"] = self.request.get_full_path()
        return super().list(self, request, *args, **kwargs)

    def get_template_names(self):
        if self.action == "list":
            return ["store/index.html"]
        if self.action == "retrieve":
            return ["store/book_details.html"]

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
