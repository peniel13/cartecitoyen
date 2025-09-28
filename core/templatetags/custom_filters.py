from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return (float(value) / float(arg)) * 100
    except (ValueError, ZeroDivisionError):
        return 0

from django import template

register = template.Library()

# 🔹 div simple (division)
@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0


# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def percent(value, arg):
    try:
        return (float(value) / float(arg)) * 100
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

# 🔹 add_class (ajout de classe CSS à un champ de formulaire)
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})



