from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    monthly_income_before_taxes = models.FloatField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 300)

class Account(models.Model):
    name = models.CharField(max_length = 20)
    cardType = models.CharField(max_length = 20)
    bank = models.CharField(max_length = 20)
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)