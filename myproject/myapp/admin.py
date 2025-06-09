from django.contrib import admin

# Register your models here.
from .models import Shoes, AvailableSizes, ShoeImages, Order, OrderItem
from django.db import models
from django import forms

class AvailableSizesInline(admin.TabularInline):
    model = AvailableSizes
    extra = 1
    fields = ('size', 'in_stock')   
    verbose_name = "Available Sizes and Stock"
    verbose_name_plural = "Add available Sizes and Stock"
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 40})},
        models.ImageField: {'widget': forms.ClearableFileInput(attrs={'style': 'width: 200px'})},
    }

class ShoeImagesInline(admin.TabularInline):
    model = ShoeImages
    extra = 1  # Cho phép thêm 1 ảnh trống
    max_num = 11  # Giới hạn nếu cần

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shoes._meta.fields if field.name != 'sku']
    inlines = [AvailableSizesInline, ShoeImagesInline]
    list_filter = ('gender', 'type', 'brand')
    search_fields = ('shoe_name', 'brand', 'type')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 60})},
        models.ImageField: {'widget': forms.ClearableFileInput(attrs={'style': 'width: 200px'})},
        models.IntegerField: {'widget': forms.NumberInput(attrs={'style': 'width: 200px'})},
    }
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(availablesizes__in_stock__gt=0).distinct()
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('shoe', 'get_shoe_name', 'quantity', 'price')
    readonly_fields = ('get_shoe_name',)
    show_change_link = True

    def get_shoe_name(self, obj):
        return obj.shoe.shoe_name if obj.shoe else "-"
    get_shoe_name.short_description = 'Tên sản phẩm'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'total', 'status', 'address', 'created_at')
    inlines = [OrderItemInline]
    search_fields = ('name', 'phone', 'address')
    list_filter = ('status', 'created_at')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 40})},
        models.ImageField: {'widget': forms.ClearableFileInput(attrs={'style': 'width: 200px'})},
    }

admin.site.register(Order, OrderAdmin)