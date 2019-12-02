from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def home(request):
    return render(request = request,
                  template_name = "shop/home.html",
                  context={"shop":shop})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'new account created: {username}')
            login(request, user)
            return (request, 'new account created:')
            #for now we redirect a message#
            #return redirect(request, 'shop/base.html')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}: {form.error_messages[msg]}')

    form = UserCreationForm
    return render(request = request,
                  template_name = "shop/register.html",
                  context={"form":form})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product})
