from rest_framework import routers
from .api_views import CourseViewSet

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = router.urls