from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from app.settings import PAYMENTS_PER_PAGE
from invoices.models import InvoiceItem, Invoice
from settings.models import CompanySettings
from .models import Payment, PaymentMethod
from .forms import PaymentForm


def payments_list(request):
    all_payments = Payment.objects.all()
    paginator = Paginator(all_payments, PAYMENTS_PER_PAGE)
    page = request.GET.get('page')

    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        payments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        payments = paginator.page(paginator.num_pages)

    context = {
        'payments': payments
    }

    return render(request, 'payments_list.html', context)


def reconcile_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Check if the payment can be reconciled (add your conditions here)
    if payment.reconciled_status == 'unreconciled':
        # Add the logic to reconcile the payment here (e.g., updating payment status, balance, etc.)
        # For example, you can set the reconciled status to 'reconciled'
        payment.reconciled_status = 'reconciled'
        payment.save()

        # Add a success message to be displayed in the template
        messages.success(request, f"Payment ID {payment_id} has been reconciled successfully.")

        # Redirect to the payment list page after reconciling the payment
        return HttpResponseRedirect(reverse('payments:payment_list'))
    else:
        # If the payment cannot be reconciled (e.g., already reconciled), handle the appropriate error or message here
        # For example, you can display an error message or redirect back to the payment detail page with a message
        messages.error(request, f"Payment ID {payment_id} cannot be reconciled because it is already reconciled.")
        return HttpResponseRedirect(reverse('payments:payment_detail', args=[payment_id]))


def resend_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Check if the payment can be resent (add your conditions here)
    if payment.reconciled_status != 'reconciled':
        # Add the logic to resend the payment here (e.g., update payment status, send notifications, etc.)
        # For example, you can set the payment_status to 'Pending' or 'Unpaid'
        payment.payment_status = 'Pending'  # Or any other appropriate status
        payment.save()

        # Add a success message to be displayed in the template
        messages.success(request, f"Payment ID {payment_id} has been resent successfully.")

        # Redirect to the payment list page after resending the payment
        return HttpResponseRedirect(reverse('payments:payment_list'))
    else:
        # If the payment cannot be resent (e.g., already reconciled), handle the appropriate error or message here
        # For example, you can display an error message or redirect back to the payment detail page with a message
        messages.error(request, f"Payment ID {payment_id} cannot be resent because it is already reconciled.")
        return HttpResponseRedirect(reverse('payments:payment_detail', args=[payment_id]))


def reverse_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Check if the payment can be reversed (add your conditions here)
    if payment.reconciled_status == 'reconciled':
        # Add the logic to reverse the payment here (e.g., updating payment status, balance, etc.)
        # For example, you can set the payment amount to 0 and change the reconciled status to 'reversed'
        payment.amount = 0
        payment.reconciled_status = 'reversed'
        payment.save()

        # Add a success message to be displayed in the template
        messages.success(request, f"Payment ID {payment_id} has been reversed successfully.")

        # Redirect to the payment list page after reversing the payment
        return HttpResponseRedirect(reverse('payments:payment_list'))
    else:
        # If the payment cannot be reversed (e.g., already reconciled), handle the appropriate error or message here
        # For example, you can display an error message or redirect back to the payment detail page with a message
        messages.error(request, f"Payment ID {payment_id} cannot be reversed because it is already reconciled.")
        return HttpResponseRedirect(reverse('payments:payment_detail', args=[payment_id]))


def make_payment(request, invoice_id=None):
    if request.method == 'POST':
        print(request.POST)
        form = PaymentForm(request.POST)
        if form.is_valid():
            invoice = form.cleaned_data['invoice']  # Get the selected invoice ID
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            payment_status = 'pending'  # form.cleaned_data['payment_status']
            balance = form.cleaned_data['balance']
            date_paid = form.cleaned_data['date_paid']
            # reconciled_status = form.cleaned_data['reconciled_status']
            reconciled_status = 'unreconciled'

            try:
                # Get the PaymentMethod instance for the selected payment method

                # Create the Payment object with the provided form data
                payment = Payment(
                    invoice=invoice,
                    amount=amount,
                    payment_method=payment_method,
                    payment_status=payment_status,
                    balance=balance,
                    date_paid=date_paid,
                    reconciled_status=reconciled_status
                )
                payment.save()

                return HttpResponse(f"Payment of ${amount} made via {payment_method}. Invoice ID: {invoice}")

            except PaymentMethod.DoesNotExist:
                return HttpResponse(f"Invalid payment method: {payment_method}")
        else:
            # Form is invalid, handle the errors here
            pass
    else:
        form = PaymentForm()
    return render(request, 'make_payment.html', {'form': form, 'invoice_id': invoice_id})


def calculate_total_amount(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    total_amount = InvoiceItem.objects.filter(invoice=invoice).aggregate(Sum('total_price'))['total_price__sum'] or 0
    return JsonResponse({'total_amount': total_amount})
