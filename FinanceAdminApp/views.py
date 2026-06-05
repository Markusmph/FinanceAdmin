from django.shortcuts import render, redirect
from .forms import CategoryForm, AccountForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'main.html', {})

def categories(request):
    return render(request, 'category_form.html', {})

def accounts(request):
    return render(request, 'account_form.html', {})

# @login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            # category.user = request.user
            category.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form})