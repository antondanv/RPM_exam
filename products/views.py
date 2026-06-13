from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product
from .forms import ProductFrom

# Create your views here.
def health_check(request):
    return JsonResponse({'status': 'ok'})

def products_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/products_list.html', {'products': products})

def product_create(request):
    if request.method == "POST":
        form = ProductFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductFrom()
    return render(request, 'products/products_form.html', {'form': form, 'product': None})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductFrom(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductFrom(instance=product)
    return render(request, 'products/products_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list.html')
    return render(request, 'products/product_confirm_delete.html', {'product': product})