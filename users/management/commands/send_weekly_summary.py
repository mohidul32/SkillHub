from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Send a weekly summary (demo)."

    def handle(self, *args, **kwargs):
        week_ago = timezone.now() - timezone.timedelta(days=7)
        new_users = User.objects.filter(date_joined__gte=week_ago).count()
        self.stdout.write(self.style.SUCCESS(
            f"Weekly Summary: New users in the last 7 days: {new_users}"
        ))
