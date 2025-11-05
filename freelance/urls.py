from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import FreelancerViewSet, GigViewSet, OrderViewSet
from . import views

router = DefaultRouter()
router.register(r'freelancers', FreelancerViewSet, basename='freelancer')
router.register(r'gigs', GigViewSet, basename='gig')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard, name='freelance_dashboard'),
]
