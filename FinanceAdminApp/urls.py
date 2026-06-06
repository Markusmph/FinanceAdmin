from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('category/', views.add_category, name='categories'),
    path('accounts/', views.accounts, name='accounts'),
]