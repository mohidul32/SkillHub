from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            group, _ = Group.objects.get_or_create(name='Students')
            instance.groups.add(group)
        elif instance.role == 'instructor':
            group, _ = Group.objects.get_or_create(name='Instructors')
            instance.groups.add(group)
