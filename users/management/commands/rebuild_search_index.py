from django.core.management.base import BaseCommand
from courses.models import Course
import time

class Command(BaseCommand):
    help = "Rebuild course search index (demo placeholder)."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting course search index rebuild...")
        for course in Course.objects.all():
            # Simulate indexing
            time.sleep(0.01)
            self.stdout.write(f"Indexed course: {getattr(course, 'title', course.pk)}")
        self.stdout.write(self.style.SUCCESS("Search index rebuild completed!"))
