from django.db import models
from django import forms
import uuid

class DateInput(forms.DateInput):
    input_type = 'date'


class League(models.Model):
    league_id = models.BigAutoField(primary_key=True, null=False,default=0)
    league_name = models.CharField(unique=True, max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.league_name
    


class Match(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    match_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    match_name = models.CharField(max_length=200, default="")
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    score = models.CharField(max_length=20, default='TBD')
    is_live = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_user_uploaded = models.BooleanField(null=True)
    match_link = models.URLField()

    def __str__(self):
        return self.match_name

    def save(self, *args, **kwargs):
        if not self.match_name:
            self.match_name = f"{self.team_1.strip()} vs {self.team_2.strip()}"
        super().save(*args, **kwargs)

class Highlight(models.Model):
    highlight_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, blank=False, null=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    body = models.TextField(default="", blank=False, null=False)
    highlight_action = models.CharField(max_length=10, blank=False, null=True,)
    match_time = models.CharField(max_length=10, default='00:00',blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=False)

    def __str__(self):
        return f"{self.match} highlight"



