from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('coffee-api', CoffeeViewSet)

urlpatterns = [
    path('cafe/', cafe_func, name='cafe'),
    path('main_menu/', CoffeeListView.as_view(), name='list_coffee'),
    path('main_menu/<int:coffee_id>/', CoffeeDetailView.as_view(), name='coffee_detail'),
    path('coffee_add/', CoffeeCreateView.as_view(), name='coffee_add'),
    path('coffee_update/<int:coffee_id>/', CoffeeUpdateView.as_view(), name='coffee_update'),
    path('coffee_delete/<int:coffee_id>/', CoffeeDeleteVeiw.as_view(), name='coffee_delete'),
    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),
    path('contact/', contact_email, name='contact_email'),
    path('ingredients/', IngredientsListView.as_view(), name='list_ingredient'),
    path('ingredients/<int:ingredient_id>/', IngredientDetailView.as_view(), name='ingredient_detail'),
    path('', include(router.urls)),
]

