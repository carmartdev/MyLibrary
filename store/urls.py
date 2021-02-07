from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("add", views.add_to_cart, name="add"),
    path("delete", views.delete_from_cart, name="delete"),
    path("cart", views.CartPage.as_view(), name="cart"),
    path("checkout", views.checkout, name="checkout"),
]
