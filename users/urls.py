from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/instructor/', views.instructor_signup, name='instructor_signup'),
]
