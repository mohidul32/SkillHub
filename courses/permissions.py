from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Allow only instructors to create/update/delete courses;
    everyone else can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and
            getattr(request.user, 'role', None) == 'Instructor'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only the owner or an admin can modify the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and (
                obj.owner == request.user or request.user.is_staff
            )
        )
