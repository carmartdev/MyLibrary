from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("cart/item/<str:item_id>/add", views.add_to_cart, name="add"),
    path("cart/item/<str:item_id>/delete", views.delete_from_cart, name="delete"),
    path("update", views.update_cart, name="update"),
    path("cart/", views.show_cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("search/", views.Search.as_view(), name="search"),
    path("book/<slug:pk>/", views.BookInfo.as_view(), name="book-info"),
]
