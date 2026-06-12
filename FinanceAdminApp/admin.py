from django.contrib import admin
from .models import Category
from .models import Account
from .models import IncomeCustomization
from .models import IncomeCustomizationWithCategory


# Register your models here.
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(IncomeCustomization)
admin.site.register(IncomeCustomizationWithCategory)