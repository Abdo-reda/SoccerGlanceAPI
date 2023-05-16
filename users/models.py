from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from matches.models import Match, League

import uuid

class SubscriptionType(models.Model):
    subscription_type_id = models.AutoField(primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=50, unique=True)


    def __str__(self):
            return self.subscription_type

class Subscription(models.Model):
    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subscription_id} for {self.subscription_type}"


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE,default=0, null=True)
    company_name = models.CharField(max_length=100)
    joined_date = models.DateField(default=timezone.now, null=False)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, editable= False)
    updated_at = models.DateTimeField(auto_now=True)
    target_link = models.URLField(null=True, default="http://127.0.0.1:8000/")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]

    def __str__(self):
        return self.company_name



class UserMatch(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('match', 'user')

    def __str__(self):
        return f"{self.match} - {self.user}"

