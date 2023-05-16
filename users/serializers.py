from rest_framework import serializers
from .models import User, Subscription, SubscriptionType

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    company_name = serializers.CharField(max_length=60)
    address = serializers.CharField(max_length=80)
    phone_number = serializers.RegexField(
        regex=r'^\+?\d{9,15}$',
        error_messages={
            'invalid': "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        }
    )

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'company_name', 'address', 'phone_number', 'password1', 'password2', 'target_link')



    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        
        # check if the email address is already in use
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email address is already in use")
        
        # check if the company name is already in use
        if User.objects.filter(company_name=data['company_name']).exists():
            raise serializers.ValidationError("Company name is already in use")
        
        # check if the phone number is already in use
        if User.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number is already in use")
        
        # check if the phone number is a valid phone number format
        # this validation is already performed by the RegexField, but an additional check doesn't hurt
        if not data['phone_number'].startswith('+'):
            raise serializers.ValidationError("Invalid phone number format")
        

        return data


    def create(self, validated_data):
        premium_plus_subscription = SubscriptionType.objects.get(subscription_type="PremiumPlus")
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        
        if self.is_valid(raise_exception=False):
            subscription = Subscription.objects.create(subscription_type=premium_plus_subscription)
            user = User.objects.create(**validated_data, subscription_id=subscription)
            user.set_password(password)
            user.save()
            return user
