# Real Estate Management System API

A Django REST Framework API for managing residential estate operations, including users, houses, occupants, and chief tenant assignments.

## Tech Stack

- **Python 3**
- **Django 5**
- **Django REST Framework**
- **MySQL**
- **Session Authentication**
- **Custom User Model with Roles**

## Features

- **User Role Management:** Admin, Owner (Landlord), and Chief Tenant roles with role-based permissions.
- **House Management:** Register, update, and manage houses with unique IDs, types, and apartment counts.
- **Occupant Management:** Add, update, or remove occupants per apartment; enforce max occupants per house.
- **Chief Tenant Assignment:** Assign and manage chief tenants for each house.
- **Authentication & Authorization:** Secure registration and login endpoints; session-based authentication.
- **RESTful API Endpoints:** CRUD for users, houses, occupants, and chief tenant assignments.

## Setup Guide

### 1. Prerequisites

- Python 3.8+
- MySQL

### 2. Clone the Repository

```bash
git clone https://github.com/thompsongboyega2019/real-estate-management-api.git
cd real-estate-management-api
```

### 3. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Setup
```bash
# Create initial migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `POST /api/auth/register/` - Register new user

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Houses
- `GET /api/houses/` - List all houses
- `POST /api/houses/` - Create new house
- `GET /api/houses/{id}/` - Get house details
- `PUT /api/houses/{id}/` - Update house
- `DELETE /api/houses/{id}/` - Delete house

### Occupants
- `GET /api/occupants/` - List all occupants
- `POST /api/occupants/` - Create new occupant
- `GET /api/occupants/{id}/` - Get occupant details
- `PUT /api/occupants/{id}/` - Update occupant
- `DELETE /api/occupants/{id}/` - Delete occupant

### Chief Tenant Assignments
- `GET /api/chief-tenant-assignments/` - List all assignments
- `POST /api/chief-tenant-assignments/` - Create new assignment
- `GET /api/chief-tenant-assignments/{id}/` - Get assignment details
- `PUT /api/chief-tenant-assignments/{id}/` - Update assignment
- `DELETE /api/chief-tenant-assignments/{id}/` - Delete assignment

## API Documentation

### Browsable API
Visit `http://127.0.0.1:8000/api/` to access the Django REST Framework browsable API interface.

### Admin Interface
Visit `http://127.0.0.1:8000/admin/` to access the Django admin interface.

## Testing the API

### Using the Browsable API
1. Open `http://127.0.0.1:8000/api/` in your browser
2. Navigate to any endpoint
3. Use the HTML forms to test POST, PUT, and DELETE operations

## Project Files Explanation

- `requirements.txt` - Python dependencies
- `manage.py` - Django management script
- `estate_management/settings.py` - Django configuration
- `estate/models.py` - Database models (User, House, Occupant, ChiefTenantAssignment)
- `estate/serializers.py` - API serializers for data validation and conversion
- `estate/views.py` - API views handling HTTP requests
- `estate/urls.py` - URL routing for the app
- `estate/admin.py` - Admin interface configuration










