from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # User class contains username, first_name, last_name, email, and password
    monthly_net_income = models.FloatField()

class Category(models.Model):
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 300)
    # user = models.ForeignKey(User, on_delete = models.CASCADE)

class Account(models.Model):
    name = models.CharField(max_length = 20)
    cardType = models.CharField(max_length = 20)
    bank = models.CharField(max_length = 20)
    # user = models.ForeignKey(Profile, on_delete = models.CASCADE)