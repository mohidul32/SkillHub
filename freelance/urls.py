from rest_framework.routers import DefaultRouter
from .views import FreelancerViewSet, GigViewSet, OrderViewSet

router = DefaultRouter()
router.register('freelancers', FreelancerViewSet)
router.register('gigs', GigViewSet)
router.register('orders', OrderViewSet)

urlpatterns = router.urls
