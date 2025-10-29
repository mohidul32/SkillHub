from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Course
from .serializers import CourseListSerializer, CourseDetailSerializer
from django.db.models import Count

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Only instructors (owner) can create/update/delete. Read allowed for all.
    We'll check instructor by request.user == obj.instructor.
    """
    def has_permission(self, request, view):
        # allow safe methods for any authenticated/anonymous as per policy
        if request.method in permissions.SAFE_METHODS:
            return True
        # to create, user must be authenticated and have role instructor
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'instructor'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().annotate(num_students=Count('students'))
    permission_classes = [IsInstructorOrReadOnly]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action in ['list']:
            return CourseListSerializer
        return CourseDetailSerializer

    def perform_create(self, serializer):
        # set instructor automatically
        serializer.save(instructor=self.request.user)
