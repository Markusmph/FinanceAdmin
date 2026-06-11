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
    name = models.CharField(max_length = 255)
    description = models.TextField(max_length = 1024)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('cash', 'Cash'),
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card')
    ]

    name = models.CharField(max_length = 255)
    bank = models.CharField(max_length = 255)
    account_type = models.CharField(max_length = 20, choices = ACCOUNT_TYPES, default = 'debit')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    balance = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0)

    def __str__(self):
        return f'{name} ({account_type} from bank {bank})'


class IncomeCustomization(models.Model):
    name = models.CharField(max_length = 255)
    periodic = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name