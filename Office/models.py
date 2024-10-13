from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    is_landloard = models.BooleanField(_("Is Landloard or landlady"), default=False)
    is_tenant = models.BooleanField(_("Is Tenant"), default=False)

class Address(models.Model):
    country = models.CharField(_("Country"), max_length=150)
    region = models.CharField(_("Region"), max_length=150, null=True, blank=True)
    city = models.CharField(_("City"), max_length=150)
    subcity = models.CharField(_("Subcity"), max_length=150)
    wereda = models.CharField(_("Wereda"), max_length=150)
    location = models.CharField(_("Location"), max_length = 100)

    def __str__(self):
     
        return self.location
    
    def get_addresse(self):
        if self.region:
            return "%s, %s, %s" % (self.city, self.region, self.country)
        else:
            return "%s, %s" % (self.city, self.country)


class Block(models.Model):
    name = models.CharField(_("Name"), max_length=200, help_text="give the building a name")
    managers = models.ManyToManyField(User, verbose_name=_("Managers"), limit_choices_to={'is_landloard': True})
    address = models.OneToOneField(Address, verbose_name=_("Address"), on_delete=models.PROTECT)
    block_code = models.CharField(_("Code"), max_length=50)
    total_floors = models.PositiveIntegerField(_("Number of Floor"))  
    total_offices = models.PositiveIntegerField(_("Number of Offices"))
    construction_year = models.PositiveIntegerField(_("Costruction year")) 
    description = models.TextField(_("Description") ,blank=True, null=True)
    
    def __str__(self):  
        return self.name
    
class Floor(models.Model):
    FLOOR_TYPE_CHOICES = [
        ('B', _('Basement')),
        ('G', _('Ground')),
        ('M', _('Mezzanine')),
        ('U', _('Upper')),
    ]

    block = models.ForeignKey(Block, verbose_name=_("Block"), related_name="floor", on_delete=models.CASCADE)
    floor_type = models.CharField(_("Floor Type"), max_length=1, choices=FLOOR_TYPE_CHOICES)
    order = models.PositiveIntegerField(_("Order"), help_text="Order of the floor in the block")
    total_offices = models.PositiveIntegerField(_("Number of Offices"))
    name = models.CharField(_("Name"), max_length=200, null=True, blank=True)

    class Meta:
        unique_together = ('order', 'block')
        ordering = ['order']
        verbose_name = _("Floor")
        verbose_name_plural = _("Floors")

    def __str__(self):
        return f"{self.name} ({self.floor_type}-{self.order})"
    
    def get_floor(self):
        return f"{self.floor_type}-{self.order}"

    # def clean(self):
    #     super().clean()
    #     if self.block.total_floors < self.order:
    #         raise ValidationError({
    #             'order': _("The order of the floor cannot exceed the total number of floors in the block.")
    #         })

   
class Office(models.Model):
    block = models.ForeignKey(Block, verbose_name=_("Block"), related_name="office", on_delete=models.PROTECT)
    floor = models.ForeignKey(Floor, verbose_name=_("Floor"),  related_name="office", on_delete=models.PROTECT)
    office_number = models.CharField(_("Ofice Number"), max_length=50, help_text="name or ID to identify the office")
    size = models.DecimalField(_("Size"), help_text="Size in square meter", max_digits=4, decimal_places=2)
    rent_price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    available_from = models.DateField(_("Available from"), help_text="day to be available for rent")
    amenities = models.TextField(_("Amenities"), help_text="Useful feature ", blank=True, null=True)
    is_available = models.BooleanField(_("Is Available for rent"), default=True)

        
    def __str__(self):  
        return f"{'Block ', self.block.name, ' Floor ', self.floor.get_floor(), ' Office Number ', self.office_number}"

class Lease(models.Model):
    office = models.OneToOneField(Office, verbose_name=_("Office"), on_delete=models.PROTECT, related_name="leases")
    tenant = models.ForeignKey(User, verbose_name=_("Tenant"), related_name="leases", limit_choices_to={'is_tenant': True}, on_delete=models.PROTECT)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"))
    rent_amount = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_("Is the contract Active"), default=True)

    def __str__(self):  
        return f"{self.office, self.tenant.get_full_name()}"
        

class Payment(models.Model):
    lease = models.ForeignKey(Lease, verbose_name=_("Lease"), on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    date = models.DateField(_("Date"), default=timezone.now)
    payment_method = models.CharField(_("Payment Method"), max_length=50)

    def __str__(self):  
        return f"{self.lease.office, self.lease.tenant.get_full_name, 'Payment' }"

class MaintenanceRequest(models.Model):
    office = models.ForeignKey(Office, verbose_name=_("Office"), on_delete=models.CASCADE, related_name="maintenance_requests")
    tenant = models.ForeignKey(User, verbose_name=_("Tenant"), on_delete=models.CASCADE, limit_choices_to={'is_tenant': True})
    description = models.TextField(_("Description"))
    date_submitted = models.DateField(_("Submition date"), default=timezone.now)
    status = models.CharField(_("Status"), max_length=50, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):  
        return f"{self.tenant.get_full_name, ' @ ',self.office, 'Maintenance Request' }"
