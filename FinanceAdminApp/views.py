from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'main.html', {})

def categories(request):
    return render(request, 'categoryForm.html', {})

def accounts(request):
    return render(request, 'accountForm.html', {})