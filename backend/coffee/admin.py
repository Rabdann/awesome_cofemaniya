from django.contrib import admin
from .models import CoffeeModel, IngredientsModel


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'volume', 'price', 'photo')
    search_fields = ('name', 'price')
    list_editable = ('description', 'price', 'photo')
    list_filter = ('price',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'photo')
    search_fields = ('name',)
    list_editable = ('description', 'price', 'photo')
    list_filter = ('price',)


admin.site.register(CoffeeModel, CoffeeAdmin)
admin.site.register(IngredientsModel, IngredientAdmin)