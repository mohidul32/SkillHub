from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # User roles
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def is_student(self):
        return self.role == 'student'

    def is_instructor(self):
        return self.role == 'instructor'

