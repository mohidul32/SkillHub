from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .tasks import generate_invoice_task

from .models import Freelancer, Gig, Order
from .serializers import FreelancerSerializer, GigSerializer, OrderSerializer


class FreelancerViewSet(viewsets.ModelViewSet):
    queryset = Freelancer.objects.all().select_related('user').prefetch_related('gigs', 'clients')
    serializer_class = FreelancerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        """Allow authenticated users to follow/favorite a freelancer."""
        freelancer = self.get_object()
        freelancer.clients.add(request.user)
        return Response({'status': 'added to favorites'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfavorite(self, request, pk=None):
        freelancer = self.get_object()
        freelancer.clients.remove(request.user)
        return Response({'status': 'removed from favorites'})


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.all().select_related('freelancer')
    serializer_class = GigSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        freelancer = get_object_or_404(Freelancer, user=self.request.user)
        serializer.save(freelancer=freelancer)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('client', 'gig__freelancer')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(client=self.request.user)
        generate_invoice_task.delay(order.pk)