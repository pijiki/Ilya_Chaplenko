from django import template
from shop.models import Category

register = template.Library()

@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)

@register.simple_tag()
def get_sorted():
    """Сортировка по цене цвету размеру"""
    sorters = [
        {
            'title': 'По цене',
            'sorters': [
                ('price', 'По возрастанию'),
                ('-price', 'По убыванию')
            ]
        },
        {
            'title': 'По цвету',
            'sorters': [
                ('color', 'От А до Я'),
                ('-color', 'От Я до А')

            ]
        },
        {
            'title': 'Размер',
            'sorters': [
                ('size', 'От возростанию'),
                ('-size', 'От убыванию')
            ]
        }
    ]
    return sorters