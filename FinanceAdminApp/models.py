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

class IncomeCustomizationWithCategory(models.Model):
    percentage = models.DecimalField(max_digits = 5, decimal_places = 2)
    category = models.ForeignKey(Category, on_delete = models.PROTECT, default = None)
    income_customization = models.ForeignKey(IncomeCustomization, on_delete = models.CASCADE, default = None)

class CreditCardTransaction(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('in', 'in'),
        ('out', 'out')
    )
    name = models.CharField(max_length = 255, default = '')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length = 5, choices = TRANSACTION_TYPES, default = 'in')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.PROTECT)
    category = models.ForeignKey(Category, on_delete = models.PROTECT)
    income_customization = models.ForeignKey(IncomeCustomizationWithCategory, on_delete = models.PROTECT)
    credit_card_transaction = models.ForeignKey(CreditCardTransaction, on_delete = models.PROTECT, default = None)

