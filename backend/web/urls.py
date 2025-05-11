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
from .views import ProductList, CartDetail, AddToCart, RemoveFromCart, home

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('cart/', CartDetail.as_view()),
    path('cart/add/', AddToCart.as_view()),
    path('cart/remove/', RemoveFromCart.as_view()),
    path('', home, name='home'),
]
