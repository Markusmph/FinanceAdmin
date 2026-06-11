from django.contrib import admin
from .models import Category
from .models import Account

# Register your models here.
admin.site.register(Category)
admin.site.register(Account)