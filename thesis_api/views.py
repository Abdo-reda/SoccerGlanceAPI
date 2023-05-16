from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def team(request):
    return render(request, 'team.html')

def pricing(request):
    return render(request, 'pricing.html')
