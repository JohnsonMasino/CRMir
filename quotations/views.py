from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from clients.models import Client
from products.models import Product
from quotations.forms import QuotationForm
from quotations.models import Quotation, QuotationItem


@login_required
def quotations_list(request):
    quotations = Quotation.objects.all()

    for quotation in quotations:
        total_amount = 0
        quotation_items = QuotationItem.objects.filter(quotation=quotation)
        for item in quotation_items:
            total_amount += item.total_price
        quotation.total_amount = total_amount

    # Debugging statement to check the queryset contents
    print("Quotations:", quotations)

    # Pagination
    page = request.GET.get('page')
    paginator = Paginator(quotations, 4)  # Show 10 quotations per page
    try:
        quotations = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        quotations = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range (e.g., 9999), show the last page
        quotations = paginator.page(paginator.num_pages)

    return render(request, 'quotations_list.html', {'quotations': quotations})


@login_required
@login_required
def create_quotation(request):
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save()
            # Save the quotation items
            for key, value in form.cleaned_data.items():
                if key.startswith("product_") and value:
                    product = Product.objects.get(id=value)
                    quantity = form.cleaned_data[f"quantity_{key.split('_')[1]}"]
                    unit_price = form.cleaned_data[f"unit_price_{key.split('_')[1]}"]
                    total_price = form.cleaned_data[f"total_price_{key.split('_')[1]}"]
                    quotation_item = QuotationItem(
                        quotation=quotation,
                        total_price=total_price,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    quotation_item.save()

            messages.success(request, 'Quotation created successfully.')
            return redirect('quotations:view_quotation', pk=quotation.pk)
        else:
            messages.error(request, 'Failed to create quotation. Please check the form and try again.')
    else:
        form = QuotationForm()

    products = Product.objects.all()
    clients = Client.objects.all()

    return render(request, 'create_quotation.html', {
        'form': form,
        'products': products,
        'clients': clients
    })


@login_required
def view_quotation(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    products = Product.objects.all()
    clients = [quotation.client]
    form = QuotationForm()
    return render(request, 'update_quotation.html', {
        'quotation': quotation,
        'quotation_items': quotation_items,
        'products': products,
        'clients': clients,
        'form': form
    })


@login_required
def update_quotation(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            form.save()

            # Save the quotation items
            for key, value in form.cleaned_data.items():
                if key.startswith("product_") and value:
                    quotation_item = QuotationItem(
                        quotation=quotation,
                        product_id=value,
                        quantity=form.cleaned_data[f"quantity_{key.split('_')[1]}"],
                        unit_price=form.cleaned_data[f"unit_price_{key.split('_')[1]}"],
                    )
                    quotation_item.save()

            messages.success(request, 'Quotation updated successfully.')
            return redirect('quotations:view_quotation', quotation_id)
        # else:
        #     messages.error(request, 'Failed to update quotation. Please check the form and try again.')
    else:
        form = QuotationForm(instance=quotation)

    products = Product.objects.all()
    clients = Client.objects.all()
    quotation_items = QuotationItem.objects.filter(quotation=quotation)

    return render(request, 'create_quotation.html', {
        'form': form,
        'quotation': quotation,
        'products': products,
        'clients': clients,
        'quotation_items': quotation_items
    })


@login_required
def delete_quotation(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    if request.method == 'POST':
        quotation.delete()
        messages.success(request, 'Quotation deleted successfully.')
        return redirect('quotations:quotations_list')
    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    total_amount = 0
    for item in quotation_items:
        total_amount += item.total_price
    quotation.total_amount = total_amount
    return render(request, 'delete_quotation.html', {'quotation': quotation})
