from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.categories, name='categories'),
    path('accounts/', views.accounts, name='accounts'),
]