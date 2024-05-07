from asgiref.sync import sync_to_async
from django.http import JsonResponse

from bot.models import Product, Category, Sorts


def jsonify_data(*fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            json_data = []
            for item in data:
                json_item = {}
                for field in fields:
                    if hasattr(item, field):
                        value = getattr(item, field)
                        if field == 'category':
                            value = value.category_name
                        elif field == 'sort':
                            value = value.sorts_name
                        elif field == 'image':
                            value = f'{str(value)}'
                        json_item[field] = value
                json_data.append(json_item)
            return json_data
        return wrapper
    return decorator


def search_sort_and_category_json_data(*fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            json_data = {}

            # Сначала собираем уникальные категории
            categories = Category.objects.all()
            category_names = [category.category_name for category in categories]

            # Затем собираем все уникальные сорта для каждой категории
            for category_name in category_names:
                category_data = []
                sorts = Sorts.objects.filter(sorts_category__category_name=category_name)
                sort_names = [sort.sorts_name for sort in sorts]
                category_data.extend(sort_names)

                # Записываем данные в словарь
                json_data[category_name] = category_data

            return json_data

        return wrapper

    return decorator


class DatabaseRequestToBot:
    @sync_to_async
    @jsonify_data('name', 'category', 'sort', 'description', 'price', 'image', 'discount', 'archived')
    def get_all_product(self):
        return Product.objects.all()

    @sync_to_async
    @search_sort_and_category_json_data('name', 'category', 'sort', 'price')
    def post_search_product(self):
        return Product.objects.all()

    @sync_to_async
    @jsonify_data('name', 'category', 'sort', 'description', 'price', 'image', 'discount', 'archived')
    def get_search_product(self, data):
        if data['sort'] and data['category']:
            return Product.objects.filter(sort__sorts_name=data['sort'], category__category_name=data['category'])
        elif not data['sort'] and data['category']:
            return Product.objects.filter(category__category_name=data['category'])
        elif data['sort'] and not data['category']:
            return Product.objects.filter(sort__sorts_name=data['sort'])
