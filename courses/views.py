from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm

@login_required
def course_list(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    return render(request, 'courses/course_details.html', {'course': course})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Add Course'})

@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)
    return redirect('course_detail', pk=course.id)

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.remove(request.user)
    return redirect('course_detail', pk=course.id)
