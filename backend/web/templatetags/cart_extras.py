from django import template
register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def calc_subtotal(items):
    return sum(item.quantity * item.product.original_price for item in items)