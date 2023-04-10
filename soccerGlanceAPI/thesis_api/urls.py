"""
URL configuration for thesis_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def test(request):
    return render(request, 'index.html')

def login_signup_view(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            # handle form1 data
        elif 'login' in request.POST:
            email = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Invalid username or password."

    return render(request, 'login_registration.html', {'error_message': error_message})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_signup/', login_signup_view, name='login_signup'),
    path('register/', login_signup_view, name='register'),
    path('login/', login_signup_view, name='login'),

    path('abdo/', test),
]



