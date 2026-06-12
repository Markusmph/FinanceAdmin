from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, CategoryForm, AccountForm, CustomUserCreationForm, IncomeCustomizationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Account, IncomeCustomization, IncomeCustomizationWithCategory
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

accounts_dict = {
    'object_plural_underscores': 'accounts',
    'object_plural_spaces': 'accounts',
    'object_singular_underscores': 'account',
    'object_singular_spaces': 'account'
}

def list_accounts(request):
    objects = Account.objects.filter(user = request.user).order_by('name')
    return render(request, 'default_list.html', {'objects': objects,} | accounts_dict)

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
    return render(request, 'default_add.html', {'form': form,} | accounts_dict)

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
    } | accounts_dict)

def delete_account(request, pk):
    Account.objects.filter(pk = pk).delete()
    return redirect('accounts')


# -----------------------Income Customizations----------------------------------
income_customizations_dict = {
    'object_plural_underscores': 'income_customizations',
    'object_pluarl_spaces': 'income customizations',
    'object_singular_underscores': 'income_customization',
    'object_singular_spaces': 'income customization'
}

def income_customizations(request):
    objects = IncomeCustomization.objects.filter(user = request.user).order_by('name')
    return render(request, 'default_list.html', {'objects': objects,} | income_customizations_dict)

def add_income_customization(request):
    if request.method == 'POST':
        form = IncomeCustomizationForm(request.POST)
        if form.is_valid():
            income_customization = form.save(commit = False)
            income_customization.user = request.user
            income_customization.save()

            category_ids = request.POST.getlist('category_pk')
            percentages = request.POST.getlist('percentage')

            for category_pk, percentage in zip(category_ids, percentages):
                category = Category.objects.get(pk = category_pk)
                IncomeCustomizationWithCategory.objects.create(
                    percentage = percentage,
                    category = category,
                    income_customization = income_customization
                )

            return redirect('income_customizations')
    elif request.method == 'GET':
        categories = Category.objects.filter(user = request.user)
        categories_count = categories.count()
        income_customization_form = IncomeCustomizationForm()
    return render(request, 'add_income_customization.html', {
        'income_customization_form': income_customization_form,
        'categories': categories,
    } | income_customizations_dict)

def edit_income_customization(request, pk):
    income_customization = get_object_or_404(IncomeCustomization, pk = pk)
    if request.method == 'POST':
        form = IncomeCustomizationForm(request.POST, instance = income_customization)
        if form.is_valid():
            form.save()
            return redirect('income_customizations')
    elif request.method == 'GET':
        form = IncomeCustomizationForm(instance = income_customization)
    return render(request, 'default_edit.html', {
        'form': form,
        'object': income_customization,
    } | income_customizations_dict)

def delete_income_customization(request, pk):
    IncomeCustomization.objects.filter(pk = pk).delete()
    return redirect('income_customizations')