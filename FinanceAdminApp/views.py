from django.shortcuts import render, redirect
from .forms import ProfileForm, CategoryForm, AccountForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def login(request):
    return render(request, 'login.html', {})

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