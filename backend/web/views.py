# from django.db.models import Q
# from django.http import Http404

# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib import messages
# from django.shortcuts import redirect

# from django.shortcuts import render
# from django.http import HttpResponse
# import requests
# from django.shortcuts import get_object_or_404
# from django.urls import reverse_lazy


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from .models import Product, Category
# from .serializers import ProductSerializer, CategorySerializer


# # def home(request):
# #     return render(request, 'home.html')
# class LatestProductsList(APIView):
#     def get(self, request, format=None):
#         products = Product.objects.all()[0:4]
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

# # class ProductDetail(APIView):
# #     def get_object(self, category_slug, product_slug):
# #         try:
# #             return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
# #         except Product.DoesNotExist:
# #             raise Http404
    
# #     def get(self, request, category_slug, product_slug, format=None):
# #         product = self.get_object(category_slug, product_slug)
# #         serializer = ProductSerializer(product)
# #         return Response(serializer.data)

# # class CategoryDetail(APIView):
# #     def get_object(self, category_slug):
# #         try:
# #             return Category.objects.get(slug=category_slug)
# #         except Category.DoesNotExist:
# #             raise Http404
    
# #     def get(self, request, category_slug, format=None):
# #         category = self.get_object(category_slug)
# #         serializer = CategorySerializer(category)
# #         return Response(serializer.data)



# #Hàm search để tìm kiếm sản phẩm
# @api_view(['POST'])
# def search(request):
#     query = request.data.get('query', '')

#     if query:
#         products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({"products": []})
    
# #Hàm sort để sắp xếp sản phẩm
# @api_view(['POST'])
# def sort(request):
#     sort_by = request.data.get('sort_by', '')

#     if sort_by:
#         products = Product.objects.order_by(sort_by)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     else:    
#         return Response({"products": []})
    
# #Hàm filter lại sắp xếp sản phẩm
# @api_view(['POST'])
# def filter(request):
#     filter_by = request.data.get('filter_by', '')    
#     if filter_by:
#         products = Product.objects.filter(category__name=filter_by)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({"products": []})
    
# # Hàm đăng nhập - người dung
# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
#     return render(request, 'accounts/login.html')

# def user_logout(request):
#     logout(request)
#     return redirect('home')
# # Hàm đăng ki - nguoi dung
# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/register.html', {'form': form})

# # Hàm xem chi tiết sản phẩm - người dung
# def product_detail(request, sku):
#     product = get_object_or_404(Product, sku=sku)
#     related_products = Product.objects.filter(
#         category=product.category
#     ).exclude(sku=sku)[:4]
    
#     context = {
#         'product': product,
#         'related_products': related_products,
#         'images': product.get_images(),
#         'sizes': product.get_sizes()
#     }
    
#     return render(request, 'products/product_detail.html', context)




from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer

def home(request):
    shoes = Product.objects.all()
    return render(request, 'home.html', {'shoes': shoes})

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('search')
        if query:
            return Product.objects.filter(shoe_name__icontains=query)
        return super().get_queryset()

class CartDetail(APIView):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_completed=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCart(APIView):
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_completed=False)
        sku = request.data.get('sku')
        size = request.data.get('size')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, pk=sku)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return Response({'message': 'Added to cart.'}, status=status.HTTP_200_OK)

class RemoveFromCart(APIView):
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_completed=False)
        sku = request.data.get('sku')
        size = request.data.get('size')
        product = get_object_or_404(Product, pk=sku)
        item = get_object_or_404(CartItem, cart=cart, product=product, size=size)
        item.delete()
        return Response({'message': 'Removed from cart.'}, status=status.HTTP_200_OK)
