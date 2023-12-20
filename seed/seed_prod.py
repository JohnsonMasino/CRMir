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
            talent = Talent.objects.update_or_create(
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



with transaction.atomic():
    CompanySettings.objects.all().delete()
    Talent.objects.all().delete() # delete and recreate talents
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
        company_account="0731026629",
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

