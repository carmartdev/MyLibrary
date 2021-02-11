from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("add", views.add_to_cart, name="add"),
    path("cart/item/<str:item_id>/delete", views.delete_from_cart, name="delete"),
    path("update", views.update_cart, name="update"),
    path("cart", views.CartPage.as_view(), name="cart"),
    path("checkout", views.checkout, name="checkout"),
]
