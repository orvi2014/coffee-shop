from django.contrib.auth.models import User
from rest_framework import serializers
from order.models import Order


class OrderUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")


class OrderSerializer(serializers.ModelSerializer):
    user = OrderUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("user", "cup_count", "lat", "long" , "date_created")
