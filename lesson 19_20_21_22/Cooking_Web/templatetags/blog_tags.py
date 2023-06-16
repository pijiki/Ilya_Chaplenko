from django import template
from Cooking_Web.models import Category

register = template.Library()

@register.simple_tag()
def get_all_categories():
    return Category.objects.all()

