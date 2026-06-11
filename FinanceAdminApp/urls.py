from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import CategoriesView

urlpatterns = [
    # Login and signup
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # App
    path('home/', views.home, name='home'),
        # Categories
        path('categories/', CategoriesView.as_view(), name='categories'),
        path('categories/add', views.add_category, name='add_category'),
        path('categories/edit/<int:pk>', views.edit_category, name='edit_category'),
    # path('categories/', views.categories, name='categories'),
        # Accounts
        path('accounts/', views.list_accounts, name='accounts'),
        path('accounts/add', views.add_account, name='add_account'),
        path('accounts/edit/<int:pk>', views.edit_account, name='edit_account'),
        path('accounts/delete/<int:pk>', views.delete_account, name='delete_account'),
    path('income_customizations/', views.income_customizations, name='income_customizations'),
    path('transactions/', views.transactions, name='transactions'),
]