from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard_home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def create_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'This username already exists.')

        else:
            User.objects.create_user(
                username=username,
                password=password
            )
            messages.success(request, 'User created successfully.')
            return redirect('create_user')

    return render(request, 'accounts/create_user.html')