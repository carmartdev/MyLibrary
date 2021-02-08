from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from store.models import Book, CartItem

class HomePage(generic.ListView):
    model = Book
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = get_cart_items(self.request)
        context["cart"] = tuple(i.book for i in cart_items)
        return context

def delete_from_cart(request):
    cart_items = get_cart_items(request)
    cart_items.filter(pk=request.POST.get("id")).delete()
    return HttpResponseRedirect(reverse("store:cart"))

def add_to_cart(request):
    book = get_object_or_404(Book, pk=request.POST.get("id"))
    cart_items = get_cart_items(request)
    if cart_items.filter(book=book).first() is None:
        sk = get_or_create_session_key(request)
        item = CartItem(book=book, session_key=sk)
        item.save()
    return HttpResponseRedirect(reverse("store:home"))

class CartPage(generic.ListView):
    model = CartItem
    template_name = "store/cart.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        sk = get_or_create_session_key(self.request)
        return queryset.filter(session_key=sk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = sum(i.quantity * i.book.price
                                     for i in get_cart_items(self.request))
        return context

def checkout(request):
    return render(request, "store/checkout.html")

def get_or_create_session_key(request):
    if request.session.session_key is None:
        request.session.create()
    return request.session.session_key

def get_cart_items(request):
    sk = get_or_create_session_key(request)
    return CartItem.objects.filter(session_key=sk)
