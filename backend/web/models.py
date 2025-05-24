# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.files.storage import FileSystemStorage

from django.core.files import File
from django.db import models
from django.conf import settings

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
    available_sizes = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'shoes'
        ordering = ('shoe_name',)
    
    def __str__(self):
        return self.shoe_name
    
    def get_absolute_url(self):
        return f'/products-details/{self.sku}/'
    
    def get_image(self):
        if self.image_urls:
            # Remove brackets and split by commas if the string looks like a list
            urls = self.image_urls.strip("[]").split(',')
            first_url = urls[0].strip().strip("'").strip('"')  # Remove extra quotes and spaces
            if not first_url.startswith('http://') and not first_url.startswith('https://'):
                return f"{settings.MEDIA_URL}{first_url.lstrip('/')}"  # Prefix with MEDIA_URL if relative
            return first_url  # Return as-is if it's an absolute URL
        return '/static/web/images/default.png'  # Fallback image

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.TextField(default='N/A')  # đặt giá trị mặc định

