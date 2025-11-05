from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Freelancer, Gig, Order
from .serializers import FreelancerSerializer, GigSerializer, OrderSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass

class FreelancerViewSet(viewsets.ModelViewSet):
    queryset = Freelancer.objects.all().prefetch_related('gigs', 'clients')
    serializer_class = FreelancerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # POST /api/v1/freelance/freelancers/{pk}/favorite/
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        freelancer = self.get_object()
        freelancer.clients.add(request.user)
        return Response({'detail': 'Favorited'}, status=status.HTTP_200_OK)

    # POST /api/v1/freelance/freelancers/{pk}/unfavorite/
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfavorite(self, request, pk=None):
        freelancer = self.get_object()
        freelancer.clients.remove(request.user)
        return Response({'detail': 'Unfavorited'}, status=status.HTTP_200_OK)

    # GET /api/v1/freelance/freelancers/me/  --> get freelancer profile by current user (if user is a freelancer)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        try:
            freelancer = Freelancer.objects.get(user=request.user)
        except Freelancer.DoesNotExist:
            return Response({'detail': 'Not a freelancer'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(freelancer, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def favorites(self, request):
        """Return freelancers favorited by current user."""
        qs = Freelancer.objects.filter(clients=request.user)
        serializer = self.get_serializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


    # GET /api/v1/freelance/freelancers/{pk}/orders/  -> orders for gigs of this freelancer (only freelancer or admin)
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def orders(self, request, pk=None):
        freelancer = self.get_object()
        # Only the freelancer owner or admins can view orders for this freelancer
        if request.user != freelancer.user and not request.user.is_superuser:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        orders_qs = Order.objects.filter(gig__freelancer=freelancer).select_related('client', 'gig')
        serializer = OrderSerializer(orders_qs, many=True)
        return Response(serializer.data)


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.select_related('freelancer').all()
    serializer_class = GigSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # If the authenticated user is a freelancer user (has Freelancer profile), use that profile
        try:
            freelancer = Freelancer.objects.get(user=self.request.user)
        except Freelancer.DoesNotExist:
            raise permissions.PermissionDenied("Only freelancers can create gigs.")
        serializer.save(freelancer=freelancer)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('client', 'gig__freelancer').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # client is the current user
        serializer.save(client=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(client=user)

@login_required
def dashboard(request):
    freelancer = Freelancer.objects.filter(user=request.user).first()
    gigs = Gig.objects.filter(freelancer=freelancer) if freelancer else []
    orders = Order.objects.filter(client=request.user)
    return render(request, 'freelance/dashboard.html', {
        'freelancer': freelancer,
        'gigs': gigs,
        'orders': orders,
    })