from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Freelancer, Gig, Order

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class GigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = ('id', 'freelancer', 'title', 'description', 'price', 'created_at')

class OrderSerializer(serializers.ModelSerializer):
    client = UserBasicSerializer(read_only=True)
    gig = GigSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'gig', 'status', 'ordered_at')

class FreelancerSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    gigs = GigSerializer(many=True, read_only=True)
    num_clients = serializers.IntegerField(source='clients.count', read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = ('id', 'user', 'bio', 'rating', 'skills', 'num_clients', 'is_favorited', 'gigs')
        read_only_fields = ('num_clients', 'is_favorited', 'gigs')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.clients.filter(pk=request.user.pk).exists()
