# Real Estate Management API

The Real Estate Management System API is a robust backend solution designed to digitize and streamline residential estate operations. Built with Django and Django REST Framework (DRF), this API empowers estate administrators, landlords, and chief tenants to efficiently manage property and occupant data in a secure, role-based environment.


## Project Structure

Based on the ERD, this API manages:
- **Users**: Property owners and tenants with different roles
- **Houses**: Properties with details like type, number, and apartment count
- **Occupants**: People living in the properties
- **Chief Tenant Assignments**: Special tenant roles for properties




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










