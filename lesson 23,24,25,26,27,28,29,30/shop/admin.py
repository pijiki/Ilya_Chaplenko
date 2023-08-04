from django.contrib import admin
from .models import Category, Product, Gallery

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Gallery, Review


admin.site.register(Gallery)
class GalleryInline(admin.TabularInline):
    """Галерея товаров"""
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return 0

    get_products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Товары"""
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'color', 'get_photo')
    list_editable = ('price', 'quantity', 'size', 'color')
    readonly_fields = ('watched',)
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    inlines = (GalleryInline,)

    def get_photo(self, obj):
        """Отображение миниатюры"""
        if obj.images.all():
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')

        else:
            return '-'

    get_photo.short_description = 'Миниатюра'



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('pk', 'author', 'created_at')
    readonly_fields = ('author', 'text', 'created_at')