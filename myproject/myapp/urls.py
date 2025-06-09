from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('products', views.all_products, name='products'),
    path('products-details/<int:sku>/', views.product_details, name='products_details'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:sku>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('aboutus/', TemplateView.as_view(template_name='aboutus.html'), name='aboutus'),
    path('', views.home, name='home'),
    path('products/men/', views.products_men, name='products_men'),
    path('products/women/', views.products_women, name='products_women'),
    path('cart/remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
]
