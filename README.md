# Django Sales CRM

A web-based Customer Relationship Management (CRM) system built with **Python and Django** to help businesses manage companies, contacts, sales deals, and daily tasks in one centralized platform.



## Overview

Django Sales CRM is designed to simplify customer relationship management and organize sales activities.

The application provides a centralized platform where users can manage business information, track sales opportunities, maintain customer relationships, and organize daily tasks.

## Features

### 1. Authentication
- User login and logout.
- Protected pages accessible only to authenticated users.

### 2. Companies Management
- Add, view and edit companies.
- Search for companies.
- Store company information such as name, industry, website, phone, email, address, and city.
- View related contacts and deals.

### 3. Contacts Management
- Create and manage contacts.
- Associate contacts with companies.
- Store contact details, including name, job title, email, and phone number.

### 4. Deals Management
- Create and manage sales opportunities.
- Link deals to companies and contacts.
- Track deal values.
- Set expected closing dates.
- Manage deal stages:
  - New
  - Qualified
  - Proposal
  - Negotiation
  - Won
  - Lost

### 5. Tasks Management
- Create and manage tasks.
- Associate tasks with contacts and deals.
- Set due dates and priorities.
- Track task completion status.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| SQLite | Relational database |
| HTML | Page structure |
| CSS | Styling |
| JavaScript | Frontend interactions |
| Git & GitHub | Version control |

## Project Structure

```text
django-sales-crm/
│
├── crm_project/
│   ├── manage.py
│   ├── crm_project/
│   ├── accounts/
│   ├── companies/
│   ├── contacts/
│   ├── deals/
│   ├── tasks/
│   └── ...
│
├── .gitignore
└── README.md
```

## Installation and Setup

Follow these steps to install and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Qosai1/django-sales-crm.git
```

### 2. Navigate to the Project Directory

```bash
cd django-sales-crm/crm_project
```

This directory should contain `manage.py`.

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install Django:

```bash
pip install Django
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

This creates and updates the database tables.

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## Running the Application

After completing the installation steps:

1. Activate the virtual environment.
2. Navigate to the directory containing `manage.py`.
3. Run the development server:

```bash
python manage.py runserver
```

4. Open the application in your browser.

## Demo Data

### What is Demo Data?

Demo data is fictional sample information used to demonstrate the application's features without manually entering records.

The project includes a script named `seed_demo.py` that populates the database with sample CRM records.

### Included Demo Records

| Entity | Number of Records |
|---|---:|
| Companies | 6 |
| Contacts | 10 |
| Deals | 11 |
| Tasks | 10 |

The demo records demonstrate the relationships between companies, contacts, deals, and tasks.

### How to Run Demo Data

Make sure:
- The virtual environment is activated.
- You are in the directory containing both `manage.py` and `seed_demo.py`.
- Database migrations have already been applied.

Run:

```bash
python seed_demo.py
```

The script will populate the database with demo records.

After successful execution, the terminal displays the number of companies, contacts, deals, and tasks in the database.

**Note:** The script uses existing matching records to help avoid duplicates when executed more than once. It does not intentionally delete existing data.

## Testing

### What is Testing?

Testing is the process of checking whether application features work as expected.

The project uses Django's automated testing framework to run tests and identify potential problems.

Tests can be used to verify functionality such as:

- Creating and managing companies.
- Associating contacts with companies.
- Managing sales deals and their stages.
- Creating tasks and updating their statuses.
- Protecting application pages from unauthenticated access.

### How to Run Tests

From the directory containing `manage.py`, execute:

```bash
python manage.py test
```

## Database

The project uses SQLite as its relational database.

The main database entities are:

- Company
- Contact
- Deal
- Task
