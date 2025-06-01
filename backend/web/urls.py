from django.urls import path
from .views import products, shoe_detail, home, add_to_cart, remove_from_cart, view_cart, search_products, checkout
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('products/', products, name='products'),
    path('products-details/<str:sku>/', shoe_detail, name='shoe_detail'),
    path('', home, name='home'),
    path('cart', view_cart, name='cart'),
    path('cart/add/<str:sku>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:sku>/', remove_from_cart, name='remove_from_cart'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('search/', search_products, name='search_products'),
    path('aboutus/', TemplateView.as_view(template_name='aboutus.html'), name='aboutus'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('createaccount/', views.create_account, name='createaccount'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('products/men/', views.products_men, name='products_men'),
    path('products/women/', views.products_women, name='products_women'),
]
