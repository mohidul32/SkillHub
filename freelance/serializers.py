from rest_framework import serializers
from .models import Freelancer, Gig, Order

class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = '__all__'


class GigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
