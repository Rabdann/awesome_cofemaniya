from rest_framework import serializers
from .models import CoffeeModel


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeModel
        fields = '__all__'
