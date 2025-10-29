from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, UserLoginForm, StudentSignUpForm, InstructorSignUpForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # deactivate until email verification
            user.save()

            send_activation_email(request, user)
            messages.success(request, "Please check your email to activate your account.")
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', {'form': form})

def send_activation_email(request, user):
    current_site = get_current_site(request)
    subject = "Activate your account"
    message = render_to_string('users/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        return render(request, 'users/activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    message = ''
    if request.user.is_instructor():
        message = "Welcome Instructor!"
    else:
        message = "Welcome Student!"
    return render(request, 'users/dashboard.html', {'message': message})

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'users/student_signup.html', {'form': form})


def instructor_signup(request):
    if request.method == 'POST':
        form = InstructorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = InstructorSignUpForm()
    return render(request, 'users/instructor_signup.html', {'form': form})
