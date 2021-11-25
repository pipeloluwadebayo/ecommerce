from django.urls import path
from  . import views
from .views import Index, store, basket


app_name = 'shop'

urlpatterns = [
    path('', store , name='store'),
    path('index/', Index.as_view(), name='homepage'),
    path('store/basket', basket , name='basket'),
    path('<slug:slug>/', views.item_detail, name='item_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]


