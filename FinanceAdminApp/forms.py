from django import forms
from .models import (
    Account,
    Category,
    CreditCardTransaction,
    Income,
    IncomeCustomization,
    IncomeCustomizationWithCategory,
    PeriodicTransaction,
    Profile,
    Transaction,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['monthly_net_income']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'bank', 'account_type']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class IncomeCustomizationForm(forms.ModelForm):
    class Meta:
        model = IncomeCustomization
        fields = ['name', 'periodic']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'date', 'amount', 'transaction_type', 'account', 'category', 'credit_card_transaction', 'periodic_transaction']

class CreditCardTransactionForm(forms.ModelForm):
    amount_paid = forms.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        disabled = True,
    )
    class Meta:
        model = CreditCardTransaction
        fields = ['name', 'date', 'amount', 'account', 'category', 'periodic', 'periodic_transaction']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['amount_paid'].initial = self.instance.amount_paid
        else:
            self.fields['amount_paid'].initial = Decimal('0')

class PeriodicTransactionForm(forms.ModelForm):
    class Meta:
        model = PeriodicTransaction
        fields = [
            'name',
            'amount',
            'periodic_type',
            'periodic_weekly_day',
            'periodic_monthly_day',
            'periodic_yearly_month',
            'periodic_yearly_day',
            'transaction_type',
            'account',
            'category',
            'income_customization'
        ]

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'date', 'amount', 'income_customization']