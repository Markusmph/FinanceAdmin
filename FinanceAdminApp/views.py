from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, CategoryForm, AccountForm, CustomUserCreationForm, IncomeCustomizationForm, TransactionForm, PeriodicTransactionForm, IncomeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Category, Account, IncomeCustomization, IncomeCustomizationWithCategory, Transaction, PeriodicTransaction, Income
from django.views.generic.list import ListView
from decimal import Decimal
# from django.contrib.auth.forms import UserCreationForm
from datetime import date

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
                if percentage:
                    percentage_converted = Decimal(percentage)
                    category = Category.objects.get(pk = category_pk)
                    IncomeCustomizationWithCategory.objects.create(
                        percentage = percentage_converted,
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
    income_customizations_with_category = IncomeCustomizationWithCategory.objects.filter(income_customization = income_customization)
    if request.method == 'POST':
        form = IncomeCustomizationForm(request.POST, instance = income_customization)
        if form.is_valid():
            form.save()

            category_ids = request.POST.getlist('category_pk')
            percentages = request.POST.getlist('percentage')

            for category_pk, percentage in zip(category_ids, percentages):
                if percentage:
                    percentage_converted = Decimal(percentage)
                    category = Category.objects.get(pk = category_pk)
                    try:
                        icwc = IncomeCustomizationWithCategory.objects.get(
                            category = category, 
                            income_customization = income_customization
                        )
                        icwc.percentage = percentage_converted
                        icwc.save()
                    except IncomeCustomizationWithCategory.DoesNotExist:
                        raise IncomeCustomizationWithCategory.DoesNotExist
            return redirect('income_customizations')
    elif request.method == 'GET':
        form = IncomeCustomizationForm(instance = income_customization)
    return render(request, 'edit_income_customization.html', {
        'form': form,
        'income_customization': income_customization,
        'income_customizations_with_category': income_customizations_with_category
    } | income_customizations_dict)

def delete_income_customization(request, pk):
    IncomeCustomization.objects.filter(pk = pk).delete()
    return redirect('income_customizations')


# -----------------------Transactions----------------------------------
transactions_dict = {
    'object_plural_underscores': 'transactions',
    'object_pluarl_spaces': 'transactions',
    'object_singular_underscores': 'transaction',
    'object_singular_spaces': 'transaction'
}
def transactions(request):
    objects = Transaction.objects.filter(user = request.user).order_by('date')
    return render(request, 'default_list.html', {'objects': objects} | transactions_dict)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit = False)
            transaction.user = request.user
            transaction.save()
            return redirect('transactions')
    else:
        form = TransactionForm()
    return render(request, 'default_add.html', {'form': form,} | transactions_dict)

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk = pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance = transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    elif request.method == 'GET':
        form = TransactionForm(instance = transaction)
    return render(request, 'default_edit.html', {
        'form': form,
        'object': transaction,
    } | transactions_dict)

def delete_transaction(request, pk):
    Transaction.objects.filter(pk = pk).delete()
    return redirect('transactions')

# -----------------------Periodic Transaction----------------------------------
periodic_transactions_dict = {
    'object_plural_underscores': 'periodic_transactions',
    'object_pluarl_spaces': 'periodic transactions',
    'object_singular_underscores': 'periodic_transaction',
    'object_singular_spaces': 'periodic transaction'
}

def periodic_transactions(request):
    periodic_transactions = PeriodicTransaction.objects.filter(user = request.user).order_by('name')
    return render(request, 'default_list.html', {'objects': periodic_transactions} | periodic_transactions_dict)

def add_periodic_transaction(request):
    if request.method == 'POST':
        form = PeriodicTransactionForm(request.POST)
        if form.is_valid():
            periodic_transaction = form.save(commit = False)
            periodic_transaction.user = request.user
            periodic_transaction.save()
            return redirect('periodic_transactions')
    else:
        form = PeriodicTransactionForm()
    return render(request, 'default_add.html', {'form': form,} | periodic_transactions_dict)

def edit_periodic_transaction(request, pk):
    periodic_transaction = get_object_or_404(PeriodicTransaction, pk = pk)
    if request.method == 'POST':
        form = PeriodicTransactionForm(request.POST, instance = periodic_transaction)
        if form.is_valid():
            form.save()
            return redirect('periodic_transactions')
    elif request.method == 'GET':
        form = PeriodicTransactionForm(instance = periodic_transaction)
    return render(request, 'default_edit.html', {'form': form, 'object': periodic_transaction} | periodic_transactions_dict)

def delete_periodic_transaction(request, pk):
    PeriodicTransaction.objects.filter(pk = pk).delete()
    return redirect('periodic_transactions')

# -----------------------Periodic Transaction----------------------------------
incomes_dict = {
    'object_plural_underscores': 'incomes',
    'object_pluarl_spaces': 'incomes',
    'object_singular_underscores': 'income',
    'object_singular_spaces': 'income'
}

def incomes(request):
    incomes = Income.objects.filter(user = request.user).order_by('date')
    return render(request, 'default_list.html', {'objects': incomes} | incomes_dict)

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit = False)
            income.user = request.user
            income.save()
        return redirect('incomes')
    elif request.method == 'GET':
        form = IncomeForm()
    return render(request, 'default_add.html', {'form': form} | incomes_dict)

def edit_income(request, pk):
    income = get_object_or_404(Income, pk = pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance = income)
        if form.is_valid():
            form.save()
        return redirect('incomes')
    elif request.method == 'GET':
        form = IncomeForm(instance = income)
    return render(request, 'default_edit.html', {'form': form, 'object': income} | incomes_dict)

def delete_income(request, pk):
    Income.objects.filter(pk = pk).delete()
    return redirect('incomes')


# -----------------------Auto add----------------------------------
def auto_add(request):
    now = date.today
    periodic_transactions = PeriodicTransaction.objects.filter(user = request.user)
    for periodic_transaction in periodic_transactions:
        if periodic_transaction.periodic_type == 'daily':
            last_daily_transaction = Transaction.objects.filter(user = request.user, periodic_transaction = periodic_transaction).order_by('date').last()
            # list_of_days = [day for day in range(last_daily_transaction, date.today)]
            # print(list_of_days)
        elif periodic_transaction.periodic_type == 'weekly':
            print('w')
        elif periodic_transaction.periodic_type == 'every15days':
            print('e')
        elif periodic_transaction.periodic_type == 'monthly':
            print('m')
        elif periodic_transaction.periodic_type == 'yearly':
            print('y')
    return redirect('home')