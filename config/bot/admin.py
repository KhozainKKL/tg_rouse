from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse

from .models import Product, Category, Sorts, Profile, OrderItem, Order


@admin.action(description='Архивировать товар')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(archived=True)


@admin.action(description='Разорхивировать товар')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]

    list_display = 'pk', 'name', 'category', 'sort', 'description_short', 'price', 'discount', 'image', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'name', 'category'
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        (None, {
            'fields': ('image',),
        }),
        (None, {
            'fields': ('category', 'sort'),
        }),
        ('Ценовые опции:', {
            'fields': ('price', 'discount'),
        }),
    ]

    @staticmethod
    def description_short(obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(Sorts)
admin.site.register(Profile)
admin.site.register(Order, OrderAdmin)
