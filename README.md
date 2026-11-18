# Vendors

A vendor listing and reservation management system for local student vendors.
Built with Django, Django templates, and PostgreSQL.

## Features (Phase 1: Account Feature)
- Registration (Customer or Vendor) with validation and hashed passwords
- Login and logout
- Role-based dashboards (Customer and Vendor)
- Profile view and edit

## Setup
1. Clone the repository.
2. Create and activate a virtual environment:
   `python -m venv venv` then `venv\Scripts\activate`
3. Install packages: `pip install -r requirements.txt`
4. Create a PostgreSQL database named `vendors_db`.
5. Copy `.env.example` to `.env` and fill in your values.
6. Run `python manage.py migrate`
7. Run `python manage.py runserver`