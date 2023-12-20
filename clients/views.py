from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm
from .models import Client


@login_required
def clients_list(request):
    clients = Client.objects.all()

    # Number of clients to display per page
    per_page = 4

    paginator = Paginator(clients, per_page)
    page = request.GET.get('page')

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        clients = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        clients = paginator.page(paginator.num_pages)

    return render(request, 'clients_list.html', {'clients': clients})


@login_required
def view_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'view_client.html', {'client': client})


@login_required
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()

            # Add success message
            messages.success(request, 'Client created successfully.')

            return redirect('clients:clients_list')
    else:
        form = ClientForm()

    return render(request, 'create_client.html', {'form': form})


@login_required
def update_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()

            # Add success message
            messages.success(request, 'Client updated successfully.')

            return redirect('clients:view_client', client_id=client_id)
    else:
        form = ClientForm(instance=client)

    return render(request, 'update_client.html', {'form': form, 'client': client})


@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()

        # Add success message
        messages.success(request, 'Client deleted successfully.')

        return redirect('clients:clients_list')

    return render(request, 'delete_client.html', {'client': client})
