from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('cart/', views.cart, name='cart'),  # ✅ This is required
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', include('orders.urls', namespace='orders')),

    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    # ADD TO CART
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    # DECREASE CART
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    # DELETE CART ITEM
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
    
]