# contracts/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from invoices.models import Invoice
from .models import Contract
from .forms import ContractForm


@login_required
def contracts_list(request):
    contracts = Contract.objects.all()

    # Set the number of contracts to display per page
    per_page = 4
    paginator = Paginator(contracts, per_page)

    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        contracts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        contracts = paginator.page(paginator.num_pages)

    return render(request, 'contracts_list.html', {'contracts': contracts})


@login_required
def create_contract(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.invoice = invoice
            contract.save()

            # Add success message
            messages.success(request, 'Contract created successfully.')

            return redirect('contracts:contracts_list')
    else:
        form = ContractForm()

    return render(request, 'create_contract.html', {'form': form, 'invoice': invoice})


@login_required
def update_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()

            # Add success message
            messages.success(request, 'Contract updated successfully.')

            return redirect('contracts:contracts_list')
    else:
        form = ContractForm(instance=contract)

    return render(request, 'update_contract.html', {'form': form, 'contract': contract})


@login_required
def delete_contract(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if request.method == 'POST':
        contract.delete()

        # Add success message
        messages.success(request, 'Contract deleted successfully.')

        return redirect('contracts:contracts_list')

    return render(request, 'delete_contract.html', {'contract': contract})


@login_required
def view_contract(request, pk):
    # Get the Contract object using the primary key (pk)
    contract = get_object_or_404(Contract, pk=pk)

    context = {
        'contract': contract,
    }

    return render(request, 'view_contract.html', context)
