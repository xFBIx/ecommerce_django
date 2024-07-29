from django.urls import path
from .views import (
    BookDetailView,
    BookListView,
    BookUpdateView,
    BookDeleteView,
)
from . import views

urlpatterns = [
    # path("", BookListView.as_view(), name="book_list"),
    path("", BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("book/new/", views.add_book, name="book-create"),
    path("book/<int:pk>/edit/", BookUpdateView.as_view(), name="book-edit"),
    path("book/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("add_to_wishlist/<int:pk>", views.add_to_wishlist, name="add_to_wishlist"),
    path("shoppingcart/", views.shoppingcart, name="shoppingcart"),
    path("remove_wishlist/<int:pk>", views.remove_wishlist, name="remove_wishlist"),
    path(
        "remove_shoppingcart/<int:pk>",
        views.remove_shoppingcart,
        name="remove_shoppingcart",
    ),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("vendors/", views.vendors, name="vendors"),
    path("vendors/<int:pk>", views.vendor_books, name="vendor_books"),
    path("checkout/", views.checkout, name="checkout"),
    path("buynow/", views.buynow, name="buynow"),
    # path("orders-customer/", views.orderscustomer, name="orders-customer"),
    path("order-history/", views.order_history, name="orders-customer"),
    path("orders-vendor/", views.ordersvendor, name="orders-vendor"),
    path(
        "orders-vendor/download-orders", views.download_orders, name="download-orders"
    ),
    path("wishlist/add-to-shoppingcart/<int:pk>/", views.addtocart, name="addtocart"),
    path("wishlist/updatecart/<int:pk>/", views.updatecart, name="updatecart"),
    path("checkout/coupon/<int:pk>/", views.coupon, name="coupon"),
    path("checkout/removecoupon/<int:pk>/", views.removecoupon, name="removecoupon"),
    path("orders-customer/review/<int:pk>/", views.review, name="review"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("FAQ/", views.FAQ, name="FAQ"),
]
