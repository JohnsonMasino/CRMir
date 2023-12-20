from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from products.forms import ProductForm


@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required
def create_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('/products')
        else:
            messages.error(request, 'Product creation failed. Please check the form.')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


@login_required
def update_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('/products')
        else:
            messages.error(request, 'Product update failed. Please check the form.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name  # Get the name of the product before deleting
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('/products')
    return render(request, 'delete_product.html', {'product': product})
