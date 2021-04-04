from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")

app_name = "store"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="store:book-list"), name="home"),
    path("cart/item/<str:item_id>/add", views.add_to_cart, name="add"),
    path("cart/item/<str:item_id>/delete", views.delete_from_cart, name="delete"),
    path("update", views.update_cart, name="update"),
    path("cart/", views.show_cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("", include(router.urls)),
]
