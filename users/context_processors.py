from django.utils import timezone
from django.contrib.auth import get_user_model
from courses.models import Course
from freelance.models import Gig

User = get_user_model()

def site_stats(request):
    """
    Provides site-wide statistics to all templates.
    """
    week_ago = timezone.now() - timezone.timedelta(days=7)
    return {
        'site_stats': {
            'total_users': User.objects.count(),
            'total_courses': Course.objects.count(),
            'total_gigs': Gig.objects.count(),
            'new_users_week': User.objects.filter(date_joined__gte=week_ago).count(),
        }
    }

def user_short(request):
    """
    Provides minimal info about the currently logged-in user.
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {'user_short': None}

    return {
        'user_short': {
            'id': user.pk,
            'username': user.username,
            'role': getattr(user, 'role', None),
        }
    }
