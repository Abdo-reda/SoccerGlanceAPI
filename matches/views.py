from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MatchForm

# Create your views here.
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def create_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            # Convert date string to datetime object
            date_str = form.cleaned_data['date'] # get the date string from the form data
            date_str = date_str.strftime('%d-%m-%Y') # convert date object to string
            date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y') # convert date string to datetime object
            if request.user.is_staff:
                form.instance.is_user_uploaded = False
            else:
                form.instance.is_user_uploaded = True
                form.instance.user_id = request.user.id


            # Update form data with converted date
            form.cleaned_data['date'] = date_obj.strftime('%Y-%m-%d') # convert datetime object to string in the desired format
            
            # Save form data to database
            form.save()
            messages.success(request,"Match added successfully!")
            return redirect('home')
        else: 
            messages.error(request,"Error with match details. Please try again.")
    else:
        form = MatchForm()
    return render(request, './match/create_match.html',{'form': form})
