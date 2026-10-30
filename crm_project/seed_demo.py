
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_project.settings")
django.setup()

from datetime import datetime, timedelta, time
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from companies.models import Company
from contacts.models import Contact
from deals.models import Deal
from tasks.models import Task


@transaction.atomic
def seed_demo():

    User = get_user_model()
    assigned_user = User.objects.filter(is_superuser=True).first()

    today = timezone.localdate()

    # -------------------------
    # 1. Companies
    # -------------------------

    companies_data = [
        ("TechNova Solutions", "Software", "Tel Aviv"),
        ("GreenLeaf Foods", "Food & Beverage", "Haifa"),
        ("BlueWave Logistics", "Logistics", "Ashdod"),
        ("MediCare Plus", "Healthcare", "Jerusalem"),
        ("BuildRight Construction", "Construction", "Beer Sheva"),
        ("Smart Retail Ltd", "Retail", "Nazareth"),
    ]

    companies = {}

    for name, industry, city in companies_data:
        company, _ = Company.objects.get_or_create(
            name=name,
            defaults={
                "industry": industry,
                "city": city,
            }
        )
        companies[name] = company

    # -------------------------
    # 2. Contacts
    # -------------------------

    contacts_data = [
        ("Dana Levi", "CTO", "dana@technova.example", "050-0000001", "TechNova Solutions"),
        ("Omer Katz", "IT Manager", "omer@technova.example", "050-0000002", "TechNova Solutions"),
        ("Rana Haddad", "Purchasing Manager", "rana@greenleaf.example", "050-0000003", "GreenLeaf Foods"),
        ("Yossi Cohen", "CEO", "yossi@greenleaf.example", "050-0000004", "GreenLeaf Foods"),
        ("Maya Mizrahi", "Operations Director", "maya@bluewave.example", "050-0000005", "BlueWave Logistics"),
        ("Dr. Sami Khoury", "Medical Director", "sami@medicare.example", "050-0000006", "MediCare Plus"),
        ("Noa Peretz", "Finance Manager", "noa@medicare.example", "050-0000007", "MediCare Plus"),
        ("Avi Ben-David", "Project Manager", "avi@buildright.example", "050-0000008", "BuildRight Construction"),
        ("Lina Saleh", "Marketing Manager", "lina@smartretail.example", "050-0000009", "Smart Retail Ltd"),
        ("Eitan Friedman", "Store Chain Manager", "eitan@smartretail.example", "050-0000010", "Smart Retail Ltd"),
    ]

    contacts = {}

    for name, job_title, email, phone, company_name in contacts_data:
        contact, _ = Contact.objects.get_or_create(
            company=companies[company_name],
            name=name,
            defaults={
                "job_title": job_title,
                "email": email,
                "phone": phone,
            }
        )
        contacts[name] = contact

    # -------------------------
    # 3. Deals
    # -------------------------

    deals_data = [
        ("CRM licenses - 50 seats", "TechNova Solutions", "Dana Levi", 45000, "negotiation", 10),
        ("Cloud backup service", "TechNova Solutions", "Omer Katz", 12000, "new", 45),
        ("Inventory system upgrade", "GreenLeaf Foods", "Rana Haddad", 28000, "proposal", 20),
        ("Annual support contract", "GreenLeaf Foods", "Yossi Cohen", 15000, "won", -5),
        ("Fleet tracking solution", "BlueWave Logistics", "Maya Mizrahi", 60000, "qualified", 30),
        ("Warehouse scanners", "BlueWave Logistics", "Maya Mizrahi", 9000, "lost", -12),
        ("Patient portal", "MediCare Plus", "Dr. Sami Khoury", 75000, "proposal", 25),
        ("Billing module", "MediCare Plus", "Noa Peretz", 22000, "won", -20),
        ("Site management app", "BuildRight Construction", "Avi Ben-David", 33000, "new", 60),
        ("Loyalty program platform", "Smart Retail Ltd", "Lina Saleh", 40000, "negotiation", 7),
        ("POS integration", "Smart Retail Ltd", "Eitan Friedman", 18000, "qualified", 35),
    ]

    deals = {}

    for title, company_name, contact_name, value, stage, days in deals_data:
        deal, _ = Deal.objects.get_or_create(
            title=title,
            company=companies[company_name],
            defaults={
                "contact": contacts[contact_name],
                "value": value,
                "stage": stage,
                "expected_close_date": today + timedelta(days=days),
                "assigned_to": assigned_user,
            }
        )
        deals[title] = deal

    # -------------------------
    # 4. Tasks
    # -------------------------

    tasks_data = [
        ("Send revised price offer", "CRM licenses - 50 seats", "Dana Levi", "high", -2, False,
         "Send the revised pricing proposal to the customer."),

        ("Call about delivery dates", "Fleet tracking solution", "Maya Mizrahi", "medium", -1, False,
         "Contact the customer to confirm delivery dates."),

        ("Demo patient portal", "Patient portal", "Dr. Sami Khoury", "high", 0, False,
         "Prepare and demonstrate the patient portal."),

        ("Follow-up email after meeting", "Inventory system upgrade", "Rana Haddad", "medium", 0, False,
         "Send a follow-up email after the meeting."),

        ("Prepare contract draft", "Loyalty program platform", "Lina Saleh", "high", 2, False,
         "Prepare the first draft of the contract."),

        ("Discovery call", "Cloud backup service", "Omer Katz", "low", 3, False,
         "Schedule a discovery call with the customer."),

        ("Technical requirements review", "POS integration", "Eitan Friedman", "medium", 5, False,
         "Review the technical requirements."),

        ("Site visit", "Site management app", "Avi Ben-David", "low", 7, False,
         "Arrange a site visit with the customer."),

        ("Send welcome package", "Annual support contract", "Yossi Cohen", "low", -4, True,
         "Send the welcome package to the customer."),

        ("Kick-off meeting", "Billing module", "Noa Peretz", "medium", -15, True,
         "Complete the kick-off meeting."),
    ]

    for title, deal_title, contact_name, priority, days, completed, description in tasks_data:

        task_date = today + timedelta(days=days)
        due_date = timezone.make_aware(
            datetime.combine(task_date, time(10, 0))
        )

        Task.objects.get_or_create(
            title=title,
            deal=deals[deal_title],
            defaults={
                "contact": contacts[contact_name],
                "priority": priority,
                "due_date": due_date,
                "is_completed": completed,
                "description": description,
            }
        )

    print("Demo data created successfully!")
    print(f"Companies: {Company.objects.count()}")
    print(f"Contacts: {Contact.objects.count()}")
    print(f"Deals: {Deal.objects.count()}")
    print(f"Tasks: {Task.objects.count()}")


if __name__ == "__main__":
    seed_demo()
