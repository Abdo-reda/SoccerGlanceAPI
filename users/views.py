from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm
from django.contrib import messages

from .models import SubscriptionType, Subscription

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(
                request, " Incorrect login details. Please try again or contact support.")
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, " Successfully logged out.")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            premium_plus_subscription = SubscriptionType.objects.filter(
                subscription_type="PremiumPlus").first()
            user.subscription_id = Subscription.objects.create(
                subscription_type=premium_plus_subscription)
            user.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(
                request, "Error with login details. Please try again.")
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register.html', {'form': form})
