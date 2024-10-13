from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Address, Block, Floor,Office, Lease, Payment, MaintenanceRequest

class AddressForm(ModelForm):
    class Meta:
         model = Address
         fields = '__all__'

class BlockForm(ModelForm):
    class Meta:
         model = Block
         exclude = ["address"]

class FloorForm(ModelForm):
    class Meta:
         model = Floor
         exclude = ["block"]
    # def clean(self):
    #     cleaned_data = super().clean()
    #     block = self.instance.block
    #     if self.user:
    #         if not (self.user.is_staff or (self.user.is_landloard and self.user in block.managers.all())):
    #             raise ValidationError(_("You do not have permission to create this floor."))

class OfficeForm(ModelForm):
    available_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
         model = Office
         exclude = ["block", "floor"]

class LeaseForm(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
         model = Lease
         exclude = ["office"]

class PaymentForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
         model = Payment
         exclude = ["lease"]


class MaintenanceRequestForm(ModelForm):
    class Meta:
         model = MaintenanceRequest
         fields = "__all__"

