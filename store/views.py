from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import filters, viewsets
from store.models import Author, Book
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
        response = super().list(self, request, *args, **kwargs)
        author_id = self.request.query_params.get("author", None)
        if author_id:
            response.data["author"] = Author.objects.get(pk=author_id).name
        search_keyword = self.request.query_params.get("search", None)
        if search_keyword:
            response.data["keyword"] = search_keyword
        return response

    def get_template_names(self):
        if self.action == "list":
            return ["store/index.html"]
        if self.action == "retrieve":
            return ["store/book_details.html"]

@require_POST
def delete_from_cart(request):
    cart = request.session.get("cart", {})
    cart.pop(request.POST["book_id"])
    request.session["cart"] = cart
    if "application/json" in get_acceptable_media_types(request):
        return JsonResponse({"message": "book deleted from cart"}, status=200)
    else:
        return redirect("store:cart")

@require_POST
def update_cart(request):
    cart = request.session.get("cart", {})
    qtys = dict((k, v) for k, v in request.POST.items() if k.startswith("qty"))
    for i, q in qtys.items():
        cart[i[4:]] = int(q)

    request.session["cart"] = cart
    if "application/json" in get_acceptable_media_types(request):
        return JsonResponse({"message": "cart updated"}, status=200)
    else:
        return redirect("store:cart")

@require_POST
def add_to_cart(request):
    book = get_object_or_404(Book, pk=request.POST["book_id"])
    cart = request.session.get("cart", {})
    cart[book.pk] = 1
    request.session["cart"] = cart
    if "application/json" in get_acceptable_media_types(request):
        return JsonResponse({"message": "book added to cart"}, status=201)
    else:
        return redirect(request.META.get("HTTP_REFERER"))

def show_cart(request):
    cart = request.session.get("cart", {})
    response = {"cart": [dict(qty=cart[book.pk],
                              total=cart[book.pk] * book.price,
                              **BookSerializer(book).data)
                         for book in Book.objects.filter(key__in=cart.keys())]}
    response["total_price"] = sum(book["total"] for book in response["cart"])
    if "application/json" in get_acceptable_media_types(request):
        return JsonResponse(response)
    else:
        return render(request, "store/cart.html", response)

def get_acceptable_media_types(request):
    return request.META.get("HTTP_ACCEPT", "*/*").split(",")

def checkout(request):
    return render(request, "store/checkout.html")
