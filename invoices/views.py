import datetime
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa

from .models import Invoice, InvoiceItem
from quotations.models import QuotationItem, Quotation
from .forms import InvoiceForm
from settings.models import CompanySettings  # Import the Settings model from the settings app


@login_required
def invoices_list(request):
    invoices = Invoice.objects.all()

    # Pagination
    page = request.GET.get('page')
    paginator = Paginator(invoices, 4)  # Show 10 invoices per page
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        invoices = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range (e.g., 9999), show the last page
        invoices = paginator.page(paginator.num_pages)

    return render(request, 'invoices_list.html', {'invoices': invoices})


@login_required
def create_invoice_view(request, quotation_id):
    quotation = get_object_or_404(Quotation, pk=quotation_id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.quotation = quotation
            invoice.save()

            # Copy quotation items to invoice items
            quotation_items = QuotationItem.objects.filter(quotation=quotation)
            for quotation_item in quotation_items:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=quotation_item.product,
                    quantity=quotation_item.quantity,
                    unit_price=quotation_item.unit_price,
                    total_price=quotation_item.total_price
                )

            # Add success message after successfully creating the invoice
            messages.success(request, "Invoice created successfully!")
            return redirect('invoices:invoices_list')
        else:
            # Add error message if the form is invalid
            messages.error(request, "Failed to create the invoice. Please check the form.")
    else:
        form = InvoiceForm()
        quotation_items = QuotationItem.objects.filter(quotation=quotation)
        settings = CompanySettings.objects.first()
        current_date = datetime.datetime.now()
        # Format the date as "yymm"
        formatted_date = current_date.strftime("%y%m")
        notes = settings.payment_terms
        invoice_reference = f"{settings.invoice_prefix}{quotation.id}{formatted_date}"

        form.invoice_notes = notes
        form.invoice_date = current_date.strftime("%Y-%m-%d")
        form.tax = settings.default_tax
        form.discount = settings.default_discount
        form.invoice_reference = invoice_reference

        data = {
            'form': form,
            'quotation': quotation,
            'quotation_items': quotation_items,
        }
        return render(request, 'create_invoice.html', data)


def render_to_pdf(html_content):
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_content), result, encoding="UTF-8")
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


@login_required
def view_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)

    # Fetch the company_name, company_address, and invoice_prefix from the Settings model
    try:
        settings = CompanySettings.objects.get(pk=1)  # Assuming there's only one settings instance
        company_name = settings.company_name
        company_address = settings.company_address
        invoice_prefix = settings.invoice_prefix
    except CompanySettings.DoesNotExist:
        # Handle the case when no settings are available
        company_name = "Your Company Name"
        company_address = "Your Company Address"
        invoice_prefix = "INV"  # Replace "INV" with your desired default invoice prefix

    invoice_number = f"{invoice_prefix}{invoice.id}"  # Combine the prefix with the invoice ID

    theme = CompanySettings.objects.first().invoice_theme

    context = {
        'invoice': invoice,
        'invoice_items': invoice_items,
        'company_name': company_name,
        'company_address': company_address,
        'invoice_number': invoice_number,
        'invoice_theme': 'invoices-css/' + theme + '.css',
        'pdf_view': True
    }
    template = 'invoice_view_' + theme + '.html'
    html_content = render(request, template, context).content

    pdf = render_to_pdf(html_content)
    if pdf:
        return pdf

    return HttpResponse("Error generating PDF", status=500)


@login_required
def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)

    # Fetch the company_name, company_address, and invoice_prefix from the Settings model
    settings = CompanySettings.objects.first()  # Assuming there's only one settings instance
    company_name = settings.company_name
    company_address = settings.company_address
    invoice_prefix = settings.invoice_prefix
    company_account = settings.company_account
    company_bank_name = settings.company_bank_name

    invoice_number = f"{invoice_prefix}{invoice.id}"  # Combine the prefix with the invoice ID

    theme = CompanySettings.objects.first().invoice_theme

    total_amount = 0

    for item in invoice_items:
        total_amount += item.total_price

    context = {
        'invoice': invoice,
        'invoice_items': invoice_items,
        'company_name': company_name,
        'company_address': company_address,
        'invoice_number': invoice_number,
        'invoice_theme': 'invoices-css/' + theme + '.css',
        'total_amount': total_amount,
        'grand_total': total_amount - (invoice.discount * total_amount) - (invoice.tax * total_amount),
        'discount_amount': invoice.discount * total_amount,
        'tax_amount': invoice.tax * total_amount,
        'discount': invoice.discount * 100,
        'tax': invoice.tax * 100,

        'company_bank_name': company_bank_name,
        'company_account': company_account
    }

    return render(request, 'invoice_view_' + theme + '.html', context)


@login_required
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        invoice.delete()
        # Add success message after successfully deleting the invoice
        messages.success(request, "Invoice deleted successfully!")
        return redirect('invoices:invoices_list')

    return render(request, 'delete_invoice.html', {'invoice': invoice})
