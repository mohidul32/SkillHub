from rest_framework import viewsets, permissions, filters
from django.db.models import Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson
from .serializers import CourseListSerializer, CourseDetailSerializer
from .pagination import CoursePagination  # optional, from courses/pagination.py

class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'instructor')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user

class CourseViewSet(viewsets.ModelViewSet):
    # annotate student count and prefetch lessons for efficiency
    queryset = Course.objects.all().annotate(num_students=Count('students')).prefetch_related(
        Prefetch('lessons', queryset=Lesson.objects.order_by('order'))
    )
    permission_classes = [IsInstructorOrReadOnly]
    lookup_field = 'pk'  # keep default

    # pagination: prefer view-level explicit paginator (falls back to DEFAULT)
    pagination_class = CoursePagination

    # filtering/search/ordering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # allow filtering by category id and instructor id
    filterset_fields = ['category', 'instructor']
    # searching by title and description
    search_fields = ['title', 'description']
    # ordering choices
    ordering_fields = ['created_at', 'title', 'price', 'num_students']
    ordering = ['-created_at']

    def get_serializer_class(self):
        # use lightweight serializer for list action (Step13 style)
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
