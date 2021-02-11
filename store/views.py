import re
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from store.models import Book

class HomePage(generic.ListView):
    model = Book
    context_object_name = "books"
    template_name = "store/index.html"

def delete_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    cart.pop(item_id)
    request.session["cart"] = cart
    return redirect("store:cart")

def update_cart(request):
    def extract_index(item_id):
        return int(re.findall(r'\d+', item_id)[0])

    cart = request.session.get("cart", {})
    qtys = dict((k, v) for k, v in request.POST.items() if k.startswith("qty"))
    for i, q in qtys.items():
        cart[extract_index(i)] = int(q)

    request.session["cart"] = cart
    return redirect("store:cart")

def add_to_cart(request):
    book = get_object_or_404(Book, pk=request.POST.get("id"))
    cart = request.session.get("cart", {})
    cart[book.pk] = 1
    request.session["cart"] = cart
    return redirect("store:home")

class CartPage(generic.ListView):
    model = Book
    context_object_name = "cart"
    template_name = "store/cart.html"

    def get_queryset(self):
        cart = self.request.session.get("cart", {})
        queryset = super().get_queryset().filter(pk__in=cart.keys())
        for item in queryset:
            item.qty = cart[str(item.pk)]
            item.total = item.qty * item.price
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = sum(i.total for i in self.get_queryset())
        return context

def checkout(request):
    return render(request, "store/checkout.html")
