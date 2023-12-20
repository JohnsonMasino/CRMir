import csv
import decimal
import random
from datetime import date
from random import randint, choice
from django.contrib.auth.models import User
from django.db import transaction
from contracts.models import Contract
from clients.models import Client, Country, Industry
from invoices.models import Invoice, InvoiceItem
from payments.models import PaymentMethod, PaymentStatus, Payment
from products.models import Product
from quotations.models import Quotation, QuotationItem
from faker import Faker
import pycountry

from settings.models import CompanySettings, Role
from talents.models import Skill, Talent

fake = Faker()


def seed_payment_methods():
    payment_methods = [
        'Cash',
        'PayPal',
        'M-Pesa',
    ]
    for pm in payment_methods:
        PaymentMethod.objects.create(name=pm)


def seed_roles():
    roles = [
        'admin',
        'talent',
        'accountant',
        'client'
    ]
    for role in roles:
        Role.objects.create(name=role)


def seed_admin():
    User.objects.create_user(
        username='meek',
        email='admin@kishea.org',
        password='password',
        is_staff=True,
        is_active=True,
        is_superuser=True
    )
    User.objects.create_user(
        username='empire-dhv',
        email='infoempiredhv@gmail.com',
        password='empireDHV',
        is_staff=True,
        is_active=True,
        is_superuser=False
    )


def create_products_from_csv():
    csv_file = 'seed/services.csv'
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            counter += 1
            name = row['name']
            description = row['description']
            price = float(row['price'])
            Product.objects.create(product_name=name,
                                   product_reference=f"{company.product_prefix}{counter}",
                                   product_description=description, unit_cost=price)
            print(f"Product {name} seeded.")


def generate_industries_csv():
    industries_data = [
        {'name': 'Technology', 'description': 'Technology and IT services and products.'},
        {'name': 'Healthcare', 'description': 'Healthcare and medical services and products.'},
        {'name': 'Education', 'description': 'Education and learning institutions and services.'},
        {'name': 'Finance', 'description': 'Financial services and banking institutions.'},
        {'name': 'Manufacturing', 'description': 'Manufacturing and production of goods.'},
        {'name': 'Retail', 'description': 'Retail and sales of consumer goods.'},
        {'name': 'Hospitality', 'description': 'Hospitality and tourism services and accommodations.'},
        {'name': 'Transportation', 'description': 'Transportation and logistics services.'},
        {'name': 'Energy', 'description': 'Energy production and utility services.'},
        {'name': 'Real Estate', 'description': 'Real estate development and property services.'},
        {'name': 'Media', 'description': 'Media, entertainment, and content production.'},
        {'name': 'Telecommunications', 'description': 'Telecommunications and networking services.'},
        {'name': 'Automotive', 'description': 'Automotive manufacturing and vehicle services.'},
        {'name': 'Agriculture', 'description': 'Agriculture, farming, and food production.'},
        {'name': 'NGO', 'description': 'Non-governmental organization promoting social causes and advocacy.'},
        {'name': 'Government', 'description': 'Government organizations and public administration.'},
        {'name': 'Construction', 'description': 'Construction and infrastructure development services.'},
        {'name': 'Consulting', 'description': 'Business consulting and advisory services.'},
        {'name': 'Fashion', 'description': 'Fashion design, apparel, and style.'},
        {'name': 'Pharmaceutical', 'description': 'Pharmaceuticals and healthcare products.'},
        {'name': 'Legal', 'description': 'Legal and law services and practices.'},
        {'name': 'Mining', 'description': 'Mining and natural resources exploration.'},
        {'name': 'Insurance', 'description': 'Insurance and risk management services.'},
        {'name': 'Education', 'description': 'Education and learning institutions and services.'},
        {'name': 'Consulting', 'description': 'Business consulting and advisory services.'},
        {'name': 'NGO', 'description': 'Non-governmental organization promoting social causes and advocacy.'},
        {'name': 'Government', 'description': 'Government organizations and public administration.'},
        {'name': 'Construction', 'description': 'Construction and infrastructure development services.'},
        {'name': 'Consulting', 'description': 'Business consulting and advisory services.'},
        {'name': 'Fashion', 'description': 'Fashion design, apparel, and style.'},
    ]

    # Create Industry objects and save them to the database
    for data in industries_data:
        Industry.objects.create(name=data['name'], description=data['description'])


def generate_countries_csv():
    for country in pycountry.countries:
        name = country.name
        # print(country)
        code = country.alpha_3
        CompanySettings.objects.all().delete()
        Country.objects.create(
            name=name,
            code=code
        )


def create_clients_from_csv():
    csv_file = 'seed/clients.csv'
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            counter += 1
            full_name = row['full_name']
            email = row['email']
            phone = row['phone']
            address = row['address']
            city = row['location']
            country = choice(Country.objects.all())
            industry = choice(Industry.objects.all())

            Client.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                country=country,
                industry=industry,
                location=city
            )
            print(f"client {full_name} seeded.")


def create_skills():
    csv_file = 'seed/skills.csv'
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Skill.objects.create(
                skill_name=row['skill_name'],
                skill_description=row['skill_description']
            )


#
#
#
#
#
def create_talent():
    csv_file = 'seed/talents.csv'
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            talent = Talent.objects.create(
                email_address=row['email'],
                address=row['country'],
                full_name=row['full_name'],
                phone_number=row['phone_number'],
                profile=row['profile'],
                resume=row['resume']
            )
            # Add skills to the talent
            talent.skills.update_or_create(
                skill_name=row['role'],
                skill_description=row['role']
            )


def seed_sample_payments():
    print('Seeding payments...')

    # Create payment methods
    payment_methods = ['Cash', 'PayPal', 'M-Pesa', 'Stripe']
    for method in payment_methods:
        PaymentMethod.objects.get_or_create(name=method)

    # Create payment statuses
    payment_statuses = ['Pending', 'Paid', 'Partially Paid', 'Reconciled', 'Failed']
    for status in payment_statuses:
        PaymentStatus.objects.get_or_create(name=status)

    # Get all Invoice to use as payment recipients

    # Create 20 payments with random data
    for _ in range(20):
        _invoice = choice(Invoice.objects.all())
        payment_method = choice(PaymentMethod.objects.all())
        _payment_status = choice(PaymentStatus.objects.all())

        amount = random.uniform(10, 500)  # Random amount between 10 and 500
        date_paid = fake.date_between(start_date='-30d', end_date='today')  # Random date within the last 30 days
        total = 0
        invoice_items = InvoiceItem.objects.filter(invoice=_invoice)
        for tot in invoice_items:
            total += tot.total_price

        balance = total - decimal.Decimal(amount)

        Payment.objects.create(
            invoice=_invoice,
            payment_method=payment_method,
            payment_status=_payment_status,
            amount=amount,
            date_paid=date_paid,
            balance=balance
        )

    print('Successfully seeded payments.')


with transaction.atomic():
    # Truncate all tables before seeding
    Contract.objects.all().delete()
    Country.objects.all().delete()
    Industry.objects.all().delete()
    InvoiceItem.objects.all().delete()
    Invoice.objects.all().delete()
    QuotationItem.objects.all().delete()
    Quotation.objects.all().delete()
    Product.objects.all().delete()
    Client.objects.all().delete()
    Talent.objects.all().delete()
    Skill.objects.all().delete()
    User.objects.all().delete()  # Delete all non-superuser users
    CompanySettings.objects.all().delete()

    Payment.objects.all().delete()
    PaymentMethod.objects.all().delete()
    Role.objects.all().delete()

    print("Truncated all tables.")

    print('seed roles and super user')
    seed_roles()
    seed_admin()
    print('done seeding roles and super users')

    print('generating countries into database')
    generate_countries_csv()
    print('done generating countries')

    print('generating industries into database')
    generate_industries_csv()
    print('done generating industries')

    company = CompanySettings.objects.create(
        company_name="Empire DHV",
        company_address="Accra, Ghana",
        invoice_prefix="INV|",  # Replace "INV" with your desired default invoice prefix
        quotation_prefix="QUO|",  # Replace "QUO" with your desired default quotation prefix
        client_prefix="CUS|",  # Replace "CUS" with your desired default client prefix
        payment_terms="Payment to be made within 30 days",  # Set your default payment terms
        product_prefix="PRD",
        contract_prefix="CNT",
        invoice_theme="estate",
        default_tax=18,
        default_discount=11,
        company_account="01008123450",
        company_bank_name="ABSA BANK GHANA",
        company_logo='static/empire-dhv-logo.png'
    )

    settings_instance = CompanySettings.objects.first()
    if settings_instance:
        print("Company Name:", settings_instance.company_name)
        print("Company Address:", settings_instance.company_address)
        print("Invoice Prefix:", settings_instance.invoice_prefix)
        # And so on for other settings fields...
    else:
        print("No Company Settings instance found.")

    create_products_from_csv()

    # SEED 30 clientS
    print("Seeding clients...")
    create_clients_from_csv()
    print('Created client data')

    create_skills()
    create_talent()
    # Create 36 Quotation instances
    print("Seeding quotations...")
    for i in range(1, 206):
        client = choice(Client.objects.all())  # Get a random client instance
        quotation = Quotation.objects.create(
            quotation_reference=f"{settings_instance.quotation_prefix}{i:03d}",
            # Generate quotation_reference as QUO001, QUO002, ...
            quotation_date='2023-07-20',  # Set the quotation date to a specific date or use a random date
            client=client,
        )
        print(f"Quotation {i} seeded.")
        # Create random QuotationItem instances for each Quotation
        for j in range(1, randint(2, 15)):  # Create 2 to 4 quotation items per quotation
            product = choice(Product.objects.all())  # Get a random Product instance
            quantity = randint(1, 10)  # Random quantity between 1 and 10
            unit_price = product.unit_cost  # Use the unit_cost from the Product instance as the unit price
            total_price = quantity * unit_price

            QuotationItem.objects.create(
                quotation=quotation,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
            )
            print(f"Quotation Item {j} for Quotation {i} seeded.")

    # Get the IDs of all quotations in the database
    quotation_ids = Quotation.objects.values_list('id', flat=True)

    # Seed invoices with random data
    with transaction.atomic():
        print("Seeding invoices...")
        for i in range(7000, 7011):
            quotation_id = choice(quotation_ids)  # Get a random Quotation ID for each invoice
            quotation = Quotation.objects.get(pk=quotation_id)  # Retrieve the Quotation instance
            invoice_reference = f"{settings_instance.invoice_prefix}{i}"
            invoice_date = date(2023, 7, i % 30)  # Set the invoice date as needed
            payment_status = choice(['Pending', 'Paid', 'Overdue'])  # Randomly select a payment status

            # Create the Invoice instance
            invoice = Invoice.objects.create(
                invoice_reference=invoice_reference,
                invoice_date=invoice_date,
                quotation=quotation,
                payment_status=payment_status,
                discount=fake.random.randint(0, 50) / 100,
                tax=fake.random.randint(0, 20) / 100,
            )

            # Copy quotation items to invoice items
            quotation_items = QuotationItem.objects.filter(quotation=quotation)
            for quotation_item in quotation_items:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=quotation_item.product,
                    quantity=quotation_item.quantity,
                    unit_price=quotation_item.unit_price,
                    total_price=quotation_item.total_price,
                )

            print(f"Invoice {i} seeded.")

    print("All invoices seeded.")

    invoice_ids = Invoice.objects.values_list('id', flat=True)
    # Seed 10 contracts with random data
    print("Seeding contracts...")
    for i in range(1, 11):
        contract_reference = f"{settings_instance.contract_prefix}{i}"
        contract_expiration_date = date(2023, 12, i)  # Set the expiration date as needed
        contract_status = choice(['active', 'inactive', 'expired'])  # Randomly select a status

        # Get a random invoice ID for each contract
        invoice_id = choice(invoice_ids)

        contract = Contract.objects.create(
            contract_reference=contract_reference,
            contract_expiration_date=contract_expiration_date,
            contract_status=contract_status,
            invoice_id=invoice_id,
        )
        print(f"Contract {i} seeded.")
    seed_sample_payments()
    seed_payment_methods()

