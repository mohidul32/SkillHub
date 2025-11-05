from django.db import models
from django.conf import settings
from courses.models import Course

class Freelancer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Course, blank=True)
    rating = models.FloatField(default=0)

    # NEW: clients who favorited / follow / have a relationship with this freelancer
    clients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_freelancers',
        blank=True,
    )

    def __str__(self):
        return self.user.username


class Gig(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_orders')
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='orders')
    status_choices = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} → {self.gig.title} ({self.status})"
