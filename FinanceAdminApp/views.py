from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, CategoryForm, AccountForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Account
from django.views.generic.list import ListView
# from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form_profile = ProfileForm(request.POST)
        form_user = CustomUserCreationForm(request.POST)
        if form_profile.is_valid() and form_user.is_valid():
            # Save user
            user = form_user.save()

            # Save Profile
            profile = form_profile.save(commit = False)
            profile.user = user
            profile.save()

            # Log the user
            return redirect('login')
    elif request.method == 'GET':
        form_profile = ProfileForm()
        form_user = CustomUserCreationForm()
    return render(request, 'signup.html', {'form_profile': form_profile, 'form_user': form_user})

def home(request):
    return render(request, 'index.html', {})

def accounts(request):
    return render(request, 'accounts.html', {})

def income_customizations(request):
    return render(request, 'income_customizations.html', {})

def transactions(request):
    return render(request, 'transactions.html', {})

# Categories
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

# -----------------------Categories----------------------------------
class CategoriesView(ListView):
    model = Category
    template_name = 'FinanceAdminApp/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

# @login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

# -----------------------Accounts----------------------------------
# class AccountsView(ListView):
#     model = Account
#     template_name = 'FinanceAdminApp/default_list.html'
#     # contect_object_name = 'objects'

#     def get_queryset(self):
#         return Account.objects.filter(user=self.request.user)

def list_accounts(request):
    objects = Account.objects.filter(user = request.user).order_by('name')
    return render(request, 'default_list.html', {
        'objects': objects,
        'object_plural': 'Accounts',
        'object_singular': 'account'
    })

def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit = False)
            account.user = request.user
            account.save()
            return redirect('accounts')
    else:
        form = AccountForm()
    return render(request, 'default_add.html', {
        'form': form,
        'object_plural': 'accounts',
        'object_singular': 'Account'
    })

def edit_account(request, pk):
    account = get_object_or_404(Account, pk = pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance = account)
        if form.is_valid():
            form.save()
            return redirect('accounts')
    elif request.method == 'GET':
        form = AccountForm(instance = account)
    return render(request, 'default_edit.html', {
        'form': form,
        'object': account,
        'object_singular': 'account',
        'object_plural': 'accounts'
    })

def delete_account(request, pk):
    Account.objects.filter(pk = pk).delete()
    return redirect('accounts')
