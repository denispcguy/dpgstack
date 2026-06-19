from django import template
from datetime import datetime, date

register = template.Library()


@register.filter
def get_field(obj, attr):
    """Get an attribute of an object dynamically from a string name with datetime formatting"""
    try:
        value = getattr(obj, attr)
        if isinstance(value, datetime):
            return value.strftime('%H.%M %d.%m.%Y')
        elif isinstance(value, date):
            return value.strftime("%d.%m.%Y")
        return value
    except AttributeError:
        return None

@register.filter
def get_item(form, name):
    return form[name]

@register.filter
def figure_order(order_in_url, field_name):
    if order_in_url == f"-{field_name}":
        return field_name
    return f"-{field_name}"
