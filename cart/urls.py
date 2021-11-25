from django.urls import path
from . import views
from .views import OrderView, CheckOut, Cart, Index, store
app_name = 'cart'
urlpatterns=[

    path('basket/', views.basket, name='basket' ),
    path('add/', views.add_basket, name='add_basket'),

    path('cart/', Cart.as_view() , name='cart'),
    path('checkouts/', CheckOut.as_view() , name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
    ]




