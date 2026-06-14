from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

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
        return f'{self.name} ({self.account_type} from bank {self.bank})'


class IncomeCustomization(models.Model):
    name = models.CharField(max_length = 255)
    periodic = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class IncomeCustomizationWithCategory(models.Model):
    percentage = models.DecimalField(max_digits = 5, decimal_places = 2)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    income_customization = models.ForeignKey(IncomeCustomization, on_delete = models.CASCADE)

class CreditCardTransaction(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('in', 'In'),
        ('out', 'Out')
    )
    name = models.CharField(max_length = 255, default = '')
    date = models.DateField(default = None)
    amount = models.DecimalField(max_digits = 20, decimal_places = 2)
    transaction_type = models.CharField(max_length = 5, choices = TRANSACTION_TYPES, default = 'in')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.PROTECT)
    category = models.ForeignKey(Category, on_delete = models.PROTECT)
    income_customization = models.ForeignKey(IncomeCustomizationWithCategory, on_delete = models.SET_NULL, null = True, blank = True)
    credit_card_transaction = models.ForeignKey(CreditCardTransaction, on_delete = models.SET_NULL, null = True, blank = True)

class PeriodicTransaction(models.Model):
    PERIODIC_TYPE = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        # ('every15days', 'Every 15 days'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    )
    DAYS = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    )
    MONTHS = (
        ('jan', 'January'),
        ('feb', 'February'),
        ('mar', 'March'),
        ('apr', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('aug', 'August'),
        ('sep', 'September'),
        ('oct', 'October'),
        ('nov', 'November'),
        ('dec', 'December')
    )
    TRANSACTION_TYPES = (
        ('in', 'In'),
        ('out', 'Out')
    )
    name = models.CharField(max_length = 255)
    amount = models.DecimalField(max_digits = 20, decimal_places = 2)
    periodic_type = models.CharField(max_length = 20, choices = PERIODIC_TYPE)
    periodic_weekly_day = models.CharField(max_length = 20, choices = DAYS, null = True, blank = True)
    periodic_monthly_day = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(31)], null = True, blank = True)
    periodic_yearly_month = models.CharField(max_length = 20, choices = MONTHS, null = True, blank = True)
    periodic_yearly_day = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(31)], null = True, blank = True)
    transaction_type = models.CharField(max_length = 5, choices = TRANSACTION_TYPES, default = 'in')
    account = models.ForeignKey(Account, on_delete = models.SET_NULL, null = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True)
    income_customization = models.ForeignKey(IncomeCustomization, on_delete = models.SET_NULL, null = True, blank = True)
