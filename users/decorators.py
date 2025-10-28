from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied. Students only.")
    return wrapper


def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'instructor':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied. Instructors only.")
    return wrapper
