# Real Estate Management API

A Django REST Framework API for managing real estate properties, users, occupants, and chief tenant assignments.

## Project Structure

Based on the ERD, this API manages:
- **Users**: Property owners and tenants with different roles
- **Houses**: Properties with details like type, number, and apartment count
- **Occupants**: People living in the properties
- **Chief Tenant Assignments**: Special tenant roles for properties

## Step-by-Step Setup Guide

### 1. Prerequisites
Make sure you have Python 3.8+ installed on your system.

### 2. Create Project Directory
\`\`\`bash
mkdir real-estate-management-api
cd real-estate-management-api
\`\`\`

### 3. Create Virtual Environment
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 4. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 5. Database Setup
\`\`\`bash
# Create initial migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
\`\`\`

### 6. Create Superuser (Admin Account)
\`\`\`bash
python manage.py createsuperuser
\`\`\`
Follow the prompts to create an admin account.

### 7. Run Development Server
\`\`\`bash
python manage.py runserver
\`\`\`

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

### Using curl (Command Line)

1. **Create a new user:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "owner"
  }'
\`\`\`

2. **Create a new house:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/houses/ \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "user-uuid-here",
    "house_type": "apartment",
    "house_number": "A101",
    "num_apartments": 4
  }'
\`\`\`

3. **Get all houses:**
\`\`\`bash
curl http://127.0.0.1:8000/api/houses/
\`\`\`

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

## Common Commands

\`\`\`bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Access Django shell
python manage.py shell
\`\`\`

## Troubleshooting

### Common Issues:

1. **Migration errors**: Delete `db.sqlite3` and migration files, then run `makemigrations` and `migrate` again
2. **Port already in use**: Use `python manage.py runserver 8080` to run on a different port
3. **Module not found**: Make sure virtual environment is activated and dependencies are installed

### Database Reset:
\`\`\`bash
# Delete database and migrations
rm db.sqlite3
rm real_estate_app/migrations/0*.py

# Recreate migrations and database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
\`\`\`

## Next Steps

1. Add authentication and permissions
2. Implement filtering and search functionality
3. Add pagination for large datasets
4. Create comprehensive tests
5. Add API documentation with Swagger/OpenAPI
6. Deploy to production server
