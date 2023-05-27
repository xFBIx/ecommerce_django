from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='customer-homepage'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('add_to_wishlist/<int:pk>', views.add_to_wishlist, name='add_to_wishlist'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('remove_wishlist/<int:pk>', views.remove_wishlist, name='remove_wishlist'),
    path('remove_shoppingcart/<int:pk>', views.remove_shoppingcart, name='remove_shoppingcart'),    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('vendors/', views.vendors, name='vendors'),
    path('vendors/<int:pk>', views.vendor_products, name='vendor_products'),
    path('checkout/', views.checkout, name='checkout'),
    path('buynow/', views.buynow, name='buynow'),
    path('orders-customer/', views.orderscustomer, name='orders-customer'),
    path('orders-vendor/', views.ordersvendor, name='orders-vendor'),
    path('orders-vendor/download-orders', views.download_orders, name='download-orders'),
    path('wishlist/add-to-shoppingcart/<int:pk>/', views.addtocart, name='addtocart'),
    path('wishlist/updatecart/<int:pk>/', views.updatecart, name='updatecart'),
    path('checkout/coupon/<int:pk>/', views.coupon, name='coupon'),
    path('checkout/removecoupon/<int:pk>/', views.removecoupon, name='removecoupon'),
    path('orders-customer/review/<int:pk>/', views.review, name='review'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('FAQ/', views.FAQ, name='FAQ'),
]