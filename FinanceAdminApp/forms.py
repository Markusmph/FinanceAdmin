from django import forms
from .models import Account, Category

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'cardType', 'bank']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']