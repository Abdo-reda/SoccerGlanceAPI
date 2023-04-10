from django.db import models
from django.contrib.auth.models import User
import uuid

class User(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    subscription_type = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    joined_date = models.DateField()
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True,primary_key=True)
    phone_number = models.CharField(max_length=20)
    hashed_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class League(models.Model):
    league_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.league_name

class Match(models.Model):
    match_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable= False)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    score = models.CharField(max_length=20)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_1} vs {self.team_2}"

class Subscription(models.Model):
    subscription_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable= False)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=50)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subscription_type} for {self.league}"

class Highlight(models.Model):
    highlight_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable= False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"{self.match} highlight"
