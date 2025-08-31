from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, House, Occupant, ChiefTenantAssignment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin configuration
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'role')}),
    )


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    """
    House admin configuration
    """
    list_display = ('house_number', 'house_type', 'owner', 'num_apartments', 'created_at')
    list_filter = ('house_type', 'created_at', 'owner')
    search_fields = ('house_number', 'owner__email', 'owner__first_name', 'owner__last_name')
    ordering = ('house_number',)
    
    fieldsets = (
        ('Property Information', {
            'fields': ('house_number', 'house_type', 'num_apartments')
        }),
        ('Ownership', {
            'fields': ('owner',)
        }),
    )


@admin.register(Occupant)
class OccupantAdmin(admin.ModelAdmin):
    """
    Occupant admin configuration
    """
    list_display = ('full_name', 'house', 'apartment_number', 'is_chief_tenant', 'move_in_date')
    list_filter = ('is_chief_tenant', 'move_in_date', 'house__house_type')
    search_fields = ('full_name', 'house__house_number', 'apartment_number')
    ordering = ('house', 'apartment_number')
    
    fieldsets = (
        ('Occupant Information', {
            'fields': ('full_name', 'apartment_number', 'is_chief_tenant')
        }),
        ('Property', {
            'fields': ('house',)
        }),
    )


@admin.register(ChiefTenantAssignment)
class ChiefTenantAssignmentAdmin(admin.ModelAdmin):
    """
    ChiefTenantAssignment admin configuration
    """
    list_display = ('user', 'house', 'assignment_date', 'is_active')
    list_filter = ('is_active', 'assignment_date', 'house__house_type')
    search_fields = ('user__email', 'house__house_number')
    ordering = ('-assignment_date',)
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('user', 'house', 'is_active')
        }),
    )
