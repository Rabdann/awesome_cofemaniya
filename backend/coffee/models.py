from django.db import models
from django.urls import reverse


class CoffeeModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    volume = models.FloatField(verbose_name='Объём')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    recipe = models.TextField(blank=True, null=True, verbose_name='Рецепт')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    exists = models.BooleanField(default=True, verbose_name='Существует ли?')
    ingredients = models.ManyToManyField('IngredientsModel', verbose_name='Ингредиенты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('coffee_detail', kwargs={'coffee_id': self.pk})


class IngredientsModel(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    exists = models.BooleanField(default=True, verbose_name='Существует ли?')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={'ingredient_id': self.pk})