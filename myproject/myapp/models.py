# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import cloudinary.models
import cloudinary
import cloudinary_storage
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField

class Shoes(models.Model):
    sku = models.AutoField(primary_key=True)
    shoe_name = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    color_general = models.TextField(blank=True, null=True)
    original_price = models.IntegerField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def get_absolute_url(self):
        return f'/products-details/{self.sku}/'
    
    # class Meta:
    #     db_table = 'myapp_shoes'
    
class ShoeImages(models.Model):
    sku = models.ForeignKey(Shoes, models.DO_NOTHING, db_column='sku')
    image = CloudinaryField('image', blank=True, null=True)

    # class Meta:
    #     db_table = 'myapp_shoeimages'

class AvailableSizes(models.Model):
    sku = models.ForeignKey(Shoes, models.DO_NOTHING, db_column='sku')
    size = models.TextField(blank=True, null=True)
    in_stock = models.IntegerField(blank=True, null=True)

    # class Meta:
    #     db_table = 'myapp_availablesizes'


class Order(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    payment = models.CharField(max_length=50)
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Đang xử lý')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()