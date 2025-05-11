# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.files.storage import FileSystemStorage

from django.core.files import File
from django.db import models

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField()

#     class Meta:
#         ordering = ('name',)
    
#     def __str__(self):
#         return self.name
    
#     def get_absolute_url(self):
#         return f'/{self.slug}/'

class Product(models.Model):
    shoe_name = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    sku =  models.TextField(blank=True, unique=True,primary_key=True)
    original_price = models.IntegerField( blank=True, null=True)
    color_general = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    in_stock = models.IntegerField(blank=True, null=True)
    available_sizes = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'shoes'  # Ánh xạ tới bảng shoes
        ordering = ('shoe_name',)
    
    def __str__(self):
        return self.shoe_name
    
    def get_absolute_url(self):
        return f'/{self.sku}/'
    
    def get_image(self):
        if self.image_urls:
            return 'http://127.0.0.1:8000' + self.image_urls
        return ''
    
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField()

#     class Meta:
#         ordering = ('name',)
    
#     def __str__(self):
#         return self.name
    
#     def get_absolute_url(self):
#         return f'/{self.slug}/'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"
    
    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.shoe_name} (Size: {self.size})"
    
    def get_total(self):
        return self.quantity * self.product.get_current_price()