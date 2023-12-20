import datetime
import json
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum

from contracts.models import Contract
from clients.models import Client
from invoices.models import Invoice
from payments.models import Payment
from products.models import Product
from quotations.models import Quotation
from talents.models import Talent


class Revenue:
    def __init__(self, day, total):
        self.day = day
        self.total = total

    @classmethod
    def create(cls, day, total):
        return cls(day, total)


def calculate_revenue_for_week(start, end):
    # Calculate the start and end dates for the two weeks
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')

    # Create Revenue objects for each day in the two weeks
    revenue_objects = []
    current_date = start_date
    while current_date <= end_date:
        revenue_objects.append(Revenue.create(current_date.strftime('%a %d %b, %y'), random.randint(30, 100)))
        current_date += datetime.timedelta(days=1)

    # Print the Revenue objects
    for revenue in revenue_objects:
        print(f"{revenue.day}, {revenue.total}")

    return revenue_objects


@login_required
def dashboard(request):
    selected_month = datetime.datetime.now().month

    # Get relevant statistics for the dashboard
    total_invoices = Invoice.objects.count()
    total_clients = Client.objects.count()
    total_contracts = Contract.objects.count()
    total_products = Product.objects.count()
    total_quotations = Quotation.objects.count()
    total_talents = Talent.objects.count()
    total_payments = Payment.objects.count()

    # Calculate statistics for charts
    paid_invoices_count = Invoice.objects.filter(payment_status='Paid').count()
    pending_invoices_count = Invoice.objects.filter(payment_status='Pending').count()
    cancelled_invoices_count = Invoice.objects.filter(payment_status='Cancelled').count()

    # Calculate revenue trend for each week of the selected month
    today = datetime.datetime.now()
    first_day_of_month = today.replace(day=1, month=selected_month)
    last_day_of_month = (first_day_of_month + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

    # Initialize an empty list to hold revenue data for each week
    revenue_by_week = []

    # Loop through each week of the selected month
    start_date = first_day_of_month
    while start_date <= last_day_of_month:
        end_date = start_date + datetime.timedelta(days=6)
        # Calculate revenue for the current week (Replace this with actual revenue data)
        # For now, we'll just use random values for demonstration purposes
        revenue_for_week = []  # calculate_revenue_for_week()
        revenue_by_week.append([revenue_for_week])

        start_date = end_date + datetime.timedelta(days=1)

    context = {
        'total_invoices': total_invoices,
        'total_clients': total_clients,
        'total_contracts': total_contracts,
        'total_products': total_products,
        'total_quotations': total_quotations,
        'total_payments': total_payments,
        'total_talents': total_talents,
        'paid_invoices_count': paid_invoices_count,
        'pending_invoices_count': pending_invoices_count,
        'cancelled_invoices_count': cancelled_invoices_count,
        'selected_month': selected_month,
        'revenue_by_week': revenue_by_week,
    }
    return render(request, 'dashboard.html', context)


@login_required
def load_chart_data(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        revenue_by_day = calculate_revenue_for_week(start_date_str, end_date_str)
        # Convert Revenue objects to dictionaries
        revenue_list = [{'day': revenue.day, 'total': revenue.total} for revenue in revenue_by_day]
        return JsonResponse({'revenue_by_day': revenue_list})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
