from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from smart_selects.db_fields import GroupedForeignKey

# параметр делающий email уникальным для каждого пользователя


class Category(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name


class Sorts(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    sorts_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sorts_name = models.CharField(max_length=50)
    sorts_position = models.IntegerField()

    class Meta:
        verbose_name = 'Сорт'
        verbose_name_plural = 'Сорта'

    def __str__(self):
        return self.sorts_name


# БАЗА ДАННЫХ ПРОДУКТОВ
class Product(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    class Meta:
        ordering = ['name', 'price']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Каталоги'

    name = models.CharField(max_length=100, verbose_name='Имя')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    sort = GroupedForeignKey(Sorts, group_field='sorts_category', verbose_name='Сорта')
    description = models.TextField(null=False, blank=True, verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')
    discount = models.SmallIntegerField(default=0, verbose_name='Скидка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    image = models.ImageField(null=True, blank=True, upload_to='sales/image/', verbose_name='Фотография')
    archived = models.BooleanField(default=False, verbose_name='Архив')

    def __str__(self) -> str:
        return f'{self.name}'

    def description_short(self) -> str:
        if len(self.description) < 70:
            return self.description
        return self.description[:70] + '...'


# БАЗА ДАННЫХ ЗАКАЗОВ
class Order(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    name = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Клиент')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_time(self):
        return self.updated.strptime('%Y.%m.%d').date() - self.created.strptime('%Y.%m.%d').date()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name='Продукт')
    price = models.IntegerField(verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)


class Profile(models.Model):
    username = models.CharField(null=True, blank=True, max_length=20, verbose_name='Логин')
    first_name = models.CharField(null=True, blank=True, max_length=20, verbose_name='Имя')
    last_name = models.CharField(null=True, blank=True, max_length=30, verbose_name='Фамилия')
    image = models.ImageField(null=True, blank=True, upload_to='sales/image/', verbose_name='Фотография')
    phone = models.CharField(blank=True, null=True, max_length=18, verbose_name='Номер телефона')
    geo = models.TextField(max_length=100, blank=True, null=True, verbose_name='Адрес')
    email_push = models.BooleanField(default=False, verbose_name='Подписка по email')
    cart = models.IntegerField(blank=True, null=True, verbose_name='Номер дебетовой карты')
    telegram_id = models.IntegerField(blank=True, null=True, verbose_name='ID Телеграмм')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
