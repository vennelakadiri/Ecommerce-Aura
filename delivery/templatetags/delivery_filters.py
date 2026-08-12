from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def commission(value, rate=0.05):
    """Calculate commission (default 5%)"""
    try:
        return float(value) * float(rate)
    except (ValueError, TypeError):
        return 0
