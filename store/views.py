from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from store.models import Book

class HomePage(generic.ListView):
    model = Book
    context_object_name = "books"
    template_name = "store/index.html"

def delete_from_cart(request):
    book_id = request.POST.get("id")
    cart = request.session.get("cart", {})
    cart.pop(book_id)
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
        queryset = super().get_queryset()
        cart = self.request.session.get("cart", {})
        return queryset.filter(pk__in=cart.keys())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        context["total_price"] = sum(Book.objects.get(pk=book_id).price * qty
                                     for book_id, qty in cart.items())
        return context

def checkout(request):
    return render(request, "store/checkout.html")
