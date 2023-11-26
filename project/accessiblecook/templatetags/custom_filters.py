# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def comma_separated_to_checkbox_list(value):
    items = value.split(',')
    return ''.join([f'<input type="checkbox" name="checkbox_name" value="{item.strip()}">{item.strip()}<br>' for item in items if item.strip()])
