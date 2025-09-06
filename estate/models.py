from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')  # <-- Ensure superusers are admins
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractUser):
    """
    User Model for the app
    """
    ROLE_CHOICES = [
        ('owner', 'Property Owner'),
        ('tenant', 'Tenant'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    date_joined = models.DateTimeField(auto_now_add=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()  # Add the UserManager here
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.role})"


class House(models.Model):
    """
    House model representing properties in the system
    """
    HOUSE_TYPE_CHOICES = [
        ('apartment', 'Apartment Building'),
        ('single_family', 'Single Family Home'),
        ('duplex', 'Duplex'),
        ('townhouse', 'Townhouse'),
        ('condo', 'Condominium'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_houses',
        limit_choices_to={'role': 'owner'}
    )
    house_type = models.CharField(max_length=50, choices=HOUSE_TYPE_CHOICES)
    house_number = models.CharField(
        max_length=20, 
        validators=[MinLengthValidator(1)],
        help_text="Street address or house number"
    )
    num_apartments = models.PositiveIntegerField(
        default=1,
        help_text="Number of apartments/units in this property"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'houses'
        verbose_name = 'House'
        verbose_name_plural = 'Houses'
        unique_together = ['house_number', 'owner']
    
    def __str__(self):
        return f"{self.house_number} ({self.house_type}) - Owner: {self.owner.email}"


class Occupant(models.Model):
    """
    Occupant model representing people living in houses
    """
    id = models.AutoField(primary_key=True)
    house = models.ForeignKey(
        House, 
        on_delete=models.CASCADE, 
        related_name='occupants'
    )
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    apartment_number = models.CharField(
        max_length=20,
        help_text="Apartment/unit number within the house"
    )
    is_chief_tenant = models.BooleanField(
        default=False,
        help_text="Whether this occupant is the chief tenant"
    )
    move_in_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'occupants'
        verbose_name = 'Occupant'
        verbose_name_plural = 'Occupants'
        unique_together = ['house', 'apartment_number']
    
    def __str__(self):
        chief_status = " (Chief Tenant)" if self.is_chief_tenant else ""
        return f"{self.full_name} - Apt {self.apartment_number}{chief_status}"


class ChiefTenantAssignment(models.Model):
    """
    ChiefTenantAssignment model for managing chief tenant assignments
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='chief_tenant_assignment',
        limit_choices_to={'role': 'tenant'}
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name='chief_tenant_assignments'
    )
    assignment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chief_tenant_assignments'
        verbose_name = 'Chief Tenant Assignment'
        verbose_name_plural = 'Chief Tenant Assignments'
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.user.email} -> {self.house.house_number} ({status})"
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure only one active chief tenant per house
        """
        if self.is_active:
            # Deactivate other chief tenant assignments for this house
            ChiefTenantAssignment.objects.filter(
                house=self.house, 
                is_active=True
            ).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


