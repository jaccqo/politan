from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Generates a range up to the specified value."""
    return range(value)

@register.filter
def subtract(value, arg):
    """Subtracts the arg from the value."""
    return value - arg