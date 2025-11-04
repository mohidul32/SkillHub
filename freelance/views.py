from rest_framework import viewsets, permissions
from .models import Freelancer, Gig, Order
from .serializers import FreelancerSerializer, GigSerializer, OrderSerializer

class FreelancerViewSet(viewsets.ModelViewSet):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    permission_classes = [permissions.IsAuthenticated]


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
