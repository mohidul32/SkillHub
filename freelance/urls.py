from rest_framework.routers import DefaultRouter
from .views import FreelancerViewSet, GigViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'freelancers', FreelancerViewSet, basename='freelancer')
router.register(r'gigs', GigViewSet, basename='gig')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = router.urls
