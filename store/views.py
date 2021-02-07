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
        context.update({"cart_items_count": CartItem.objects.count()})
        return context

def add_to_cart(request):
    book = get_object_or_404(Book, pk=request.POST.get("id"))
    if CartItem.objects.filter(book=book).first() is None:
        item = CartItem(book=book)
        item.save()
    return HttpResponseRedirect(reverse("store:home"))

class CartPage(generic.ListView):
    model = CartItem
    template_name = "store/cart.html"

def checkout(request):
    return render(request, "store/checkout.html")
