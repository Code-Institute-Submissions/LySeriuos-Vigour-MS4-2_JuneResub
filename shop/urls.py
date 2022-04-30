from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='products'),
    # use 'int' otherwise 'add/' can be read as product id
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]
