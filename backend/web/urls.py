# from django.urls import path, include

# from web import views
# from django.contrib import admin
# from .views import home
# urlpatterns = [
#     path ('web/', views.home, name='home'),
#     path('latest-products/', views.LatestProductsList.as_view()),
#     path('web/search/', views.search),
#     path('web/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
#     path('web/<slug:category_slug>/', views.CategoryDetail.as_view()),
# ]

from django.urls import path
from .views import products, shoe_detail, home, add_to_cart, remove_from_cart, view_cart
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('products/', products, name='products'),
    path('products-details/<str:sku>/', shoe_detail, name='shoe_detail'),
    path('', home, name='home'),
    path('cart', view_cart, name='cart'),
    path('cart/add/<str:sku>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:sku>/', remove_from_cart, name='remove_from_cart'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')
]
