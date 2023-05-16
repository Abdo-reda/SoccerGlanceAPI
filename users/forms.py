from django.contrib.auth.forms import UserCreationForm

from .models import User, SubscriptionType
from django.core.validators import RegexValidator
from django import forms

class RegisterUserForm(UserCreationForm):
    # Validators   
    phone_regex = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    #Fields
    email=forms.EmailField(widget=forms.TextInput(attrs={'name': 'email', 'placeholder': 'example@example.com'}))
    company_name= forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=80, widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}))
    target_link= forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(validators=[phone_regex], widget=forms.TextInput(attrs={'class': 'form-control'})) 

    class Meta:
        model = User
        fields = ( 'company_name', 'email', 'password1', 'password2', 'phone_number', 'address', 'target_link')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['target_link'].widget.attrs['class'] = 'form-control'


        self.fields['company_name'].widget.attrs['placeholder'] = 'Company Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['address'].widget.attrs['placeholder'] = 'Address'
        self.fields['target_link'].widget.attrs['placeholder'] = 'URL Endpoint for Receiving Highlights'

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        if commit:
            user.save()
            premium_plus_subscription = SubscriptionType.objects.filter(subscription_type="PremiumPlus").first()
            user.subscription_type = premium_plus_subscription
            user.save()
        return user
