from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Address, Block, Floor,Office, Lease, Payment, MaintenanceRequest

User = get_user_model()

ADMIN_REORDER = (
    ('Office', ('Address', 'Block', 'Floor','Office', 'Lease', 'Payment', 'MaintenanceRequest')),

)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_full_name', 'email', 'is_staff', 'is_tenant']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser', 'is_tenant']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['get_addresse', 'subcity', 'wereda', 'location']
    search_fields = ['city', 'wereda']
    list_filter = ['country', 'region', 'city']

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['block_code', 'name', 'total_floors', 'total_offices', 'address']
    search_fields = ['name', 'block_code', 'address']
    list_filter = ['construction_year', 'address', 'total_offices']

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['get_floor', 'name', 'block', 'floor_type', 'total_offices']
    search_fields = ['name', 'block', 'floor_type']
    list_filter = ['floor_type', 'block', 'total_offices']

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ['office_number', 'floor', 'block', 'rent_price', 'is_available']
    search_fields = ['office_number', 'floor', 'block', 'amenities']
    list_filter = ['floor', 'size', 'rent_price', 'is_available']

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['office', 'tenant', 'rent_amount', 'is_active']
    search_fields = ['office', 'tenant', 'block']
    list_filter = ['office', 'start_date', 'end_date', 'is_active']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['lease', 'date', 'payment_method']
    search_fields = ['lease', 'date', 'payment_method']
    list_filter = ['lease', 'date', 'payment_method']

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['office', 'tenant', 'date_submitted', 'status']
    search_fields = ['office', 'tenant', 'description']
    list_filter = ['office', 'date_submitted', 'status']





