# users/tasks.py
from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task(bind=True, name='users.send_activation_email')
def send_activation_email_task(self, user_pk):
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return f'user {user_pk} does not exist'

    current_site = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')
    # Prepare activation content
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    subject = "Activate your SkillHub account"
    message = render_to_string('users/account_activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': uid,
        'token': token,
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'
    email.send()
    return f'activation email sent to {user.email}'
