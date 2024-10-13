from math import floor
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods

from .models import Address, Block, Floor,Office, Lease, Payment, MaintenanceRequest 
from .forms import AddressForm, BlockForm, FloorForm, LeaseForm, OfficeForm, PaymentForm

User = get_user_model()

#Main
def dashboard_view(request):
  
  block = Block.objects.all()
  block_headers = ['name', 'managers', 'address', 'block_code', 'total_floors', 'total_offices', 'construction_year', 'description']
  office = Office.objects.all()
  offices_with_lease = Office.objects.filter(leases__isnull=False)
  offices_without_lease = Office.objects.filter(leases__isnull=True)
  floor = Floor.objects.all()
  lease = Lease.objects.all()
  address = Address.objects.all()

  context = {
    'blocks': block,
    'block_headers': block_headers,
    'office': office,
    'office_with_lease': offices_with_lease,
    'office_without_lease': offices_without_lease,
    'floor': floor,
    'lease': lease,
    'address': address,
  }
  return render(request, 'dashboard.html', context)


#Block
def block_detail(request, pk):
    blocks = Block.objects.all()
    block = get_object_or_404(Block, pk=pk)
    floor = Floor.objects.filter(block=block)
    office = Office.objects.filter(block=block)
    offices_with_lease = office.filter(leases__isnull=False)
    offices_without_lease = office.filter(leases__isnull=True)
    lease = Lease.objects.filter(office__block=block)

    context = {
      'blocks': blocks,
      'building_block': block,
      'floor': floor,
      'office': office,
      'office_with_lease': offices_with_lease,
      'office_without_lease': offices_without_lease,
      'lease': lease
    }
    return render(request, 'block/detail.html', context)

@require_http_methods(["GET", "POST"])
def block_create(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        block_form = BlockForm(request.POST)
        print("Post")
        if address_form.is_valid() and block_form.is_valid:
            address = address_form.save()
            block = block_form.save(commit=False)
            block.address = address  
            block.save()
            return redirect('block/detail', block.pk) 
    else:
        blocks = Block.objects.all()
        block_form = BlockForm()
        address_form = AddressForm()
        context = {
            'blocks': blocks,
            'block_form': block_form,
            'address_form': address_form
        }
        return render(request, 'block/create.html', context)
  
@require_http_methods(["GET", "POST"])
def block_update(request, pk):
    blocks = Block.objects.all()
    block = get_object_or_404(Block, pk=pk)
    address = get_object_or_404(Address, pk=block.address.pk)
    if request.method == 'POST':
        block_form = BlockForm(request.POST, instance=block)
        address_form = AddressForm(request.POST, instance=address)
        if address_form.is_valid() and block_form.is_valid:
            address = address_form.save()
            block = block_form.save(commit=False)
            block.address = address  
            block.save()
            return redirect('block/detail', block.pk)  # Redirect to the detail view
    else:
        block_form = BlockForm(instance=block)
        address_form = AddressForm(instance=address)
        context = {
            'blocks': blocks,
            'update_block': block,
            'block_form': block_form,
            'address_form': address_form
        }
    return render(request, 'block/update.html', context)

@require_http_methods(["POST"])
def block_delete(request, pk):
    block = get_object_or_404(Block, pk=pk)
    block.delete()
    return redirect('dashboard')

#floor
def floor_detail(request, block_id, pk):
    blocks = Block.objects.all()
    block = get_object_or_404(Block, pk=block_id)
    floor = get_object_or_404(Floor, pk=pk)
    office = Office.objects.filter(floor=floor)
    offices_with_lease = office.filter(leases__isnull=False)
    offices_without_lease = office.filter(leases__isnull=True)
    lease = Lease.objects.filter(office__floor=floor)

    context = {
      'blocks': blocks,
      'building_block': block,
      'floor': floor,
      'office': office,
      'office_with_lease': offices_with_lease,
      'office_without_lease': offices_without_lease,
      'lease': lease
    }
    return render(request, 'floor/detail.html', context)

@require_http_methods(["GET", "POST"])
def floor_create(request, block_id):
    if request.method == 'POST':
        floor_form = FloorForm(request.POST)
        block = get_object_or_404(Block, pk=block_id)

        if floor_form.is_valid():
            floor = floor_form.save(commit=False)
            floor.block = block  

            floor_form.save()  # Perform the permission check and save the Floor
            return redirect('floor_detail', block.pk, floor.id)  # Redirect to block detail view

    else:
        blocks = Block.objects.all()
        block = get_object_or_404(Block, pk=block_id)
        floor_form = FloorForm()

        context = {
            'blocks': blocks,
            'selected_block': block,
            'floor_form': floor_form
        }
        return render(request, 'floor/create.html', context)
  
@require_http_methods(["GET", "POST"])
def floor_update(request, block_id, pk):
    blocks = Block.objects.all()
    floor = get_object_or_404(Floor, pk=pk)
    if request.method == 'POST':
        floor_form = FloorForm(request.POST, instance=floor)
        if floor_form.is_valid():
            floor = floor_form.save()
            floor.save()
            return redirect('floor_detail',floor.block.pk, floor.pk)  # Redirect to the detail view
    else:
        floor_form = FloorForm(instance=floor)
        context = {
            'blocks': blocks,
            'floor': floor,
            'floor_form': floor_form,
        }
    return render(request, 'floor/update.html', context)



#Office
def office_detail(request, block_id, floor_id, pk):
    blocks = Block.objects.all()
    office = get_object_or_404(Office, pk=pk)
    block = get_object_or_404(Block, pk=block_id)
    floor = get_object_or_404(Floor, pk=floor_id)
    lease = Lease.objects.filter(office = office)


    context = {
      'blocks': blocks,
      'office_block': block,
      'office_floor': floor,
      'office': office,
      'lease': lease
    }
    return render(request, 'office/detail.html', context)


@require_http_methods(["GET", "POST"])
def office_create(request, block_id, floor_id):
    if request.method == 'POST':
        office_form = OfficeForm(request.POST)
        floor = get_object_or_404(Floor, pk=floor_id)
        block = get_object_or_404(Block, pk=block_id)

        if office_form.is_valid():
            office = office_form.save(commit=False)
            office.block = block
            office.floor = floor  

            office_form.save()  # Perform the permission check and save the Floor
            return redirect('ofice_detail', block.pk, floor.pk, office.pk)  # Redirect to block detail view

    else:
        blocks = Block.objects.all()
        floor = get_object_or_404(Floor, pk=floor_id)
        block = get_object_or_404(Block, pk=block_id)
        office_form = OfficeForm()

        context = {
            'blocks': blocks,
            'office_block': block,
            'office_floor': floor,
            'office_form': office_form
        }
        return render(request, 'office/create.html', context)
  
@require_http_methods(["GET", "POST"])
def office_update(request, block_id, floor_id, pk):
    blocks = Block.objects.all()
    office = get_object_or_404(Office, pk=pk)
    floor = get_object_or_404(Floor, pk=floor_id)

    if request.method == 'POST':
        office_form = OfficeForm(request.POST, instance=office)
        if office_form.is_valid():
            office = office_form.save()
            office.save()
            return redirect('office_detail', block_id, floor_id, office.pk)  # Redirect to the detail view
    else:
        office_form = OfficeForm(instance=office)
        context = {
            'blocks': blocks,
            'office': office,
            'office_form': office_form,
        }
    return render(request, 'office/update.html', context)


#Lease
def lease_detail(request, block_id, floor_id, office_id, pk):
    blocks = Block.objects.all()
    office = get_object_or_404(Office, pk=office_id)
    block = get_object_or_404(Block, pk=block_id)
    floor = get_object_or_404(Floor, pk=floor_id)
    lease = get_object_or_404(Lease, pk=pk)


    context = {
      'blocks': blocks,
      'office_block': block,
      'office_floor': floor,
      'office': office,
      'lease': lease
    }
    return render(request, 'lease/detail.html', context)


@require_http_methods(["GET", "POST"])
def lease_create(request, block_id, floor_id, office_id):
    if request.method == 'POST':
        lease_form = LeaseForm(request.POST)
        office = get_object_or_404(Office, pk=office_id)

        if lease_form.is_valid():
            lease = lease_form.save(commit=False)
            lease.office = office

            lease.save()  
            return redirect('lease_detail', office.block.pk, office.floor.pk, office.pk, lease.pk)  # Redirect to block detail view

    else:
        blocks = Block.objects.all()
        office = get_object_or_404(Office, pk=office_id)
        lease_form = LeaseForm()

        context = {
            'blocks': blocks,
            'lease_form': lease_form
        }
        return render(request, 'lease/create.html', context)
  
@require_http_methods(["GET", "POST"])
def lease_update(request, block_id, floor_id, office_id, pk):
    blocks = Block.objects.all()
    office = get_object_or_404(Office, pk=office_id)
    lease = get_object_or_404(Lease, pk=pk)

    if request.method == 'POST':
        lease_form = LeaseForm(request.POST, instance=lease)
        if lease_form.is_valid():
            lease = lease_form.save()
            lease.save()
            return redirect('lease_detail', office.block.id, office.floor.id, office.pk, lease.pk)  # Redirect to the detail view
    else:
        lease_form = LeaseForm(instance=lease)
        context = {
            'blocks': blocks,
            'lease': lease,
            'lease_form': lease_form,
        }
    return render(request, 'lease/update.html', context)

#Payment
def payment_detail(request, block_id, floor_id, office_id, lease_id, pk):
    blocks = Block.objects.all()
    office = get_object_or_404(Office, pk=office_id)
    block = get_object_or_404(Block, pk=block_id)
    floor = get_object_or_404(Floor, pk=floor_id)
    lease = get_object_or_404(Lease, pk=lease_id)
    payment = get_object_or_404(Payment, pk=pk)


    context = {
      'blocks': blocks,
      'office_block': block,
      'office_floor': floor,
      'office': office,
      'lease': lease,
      'payment': payment
    }
    return render(request, 'payment/detail.html', context)


@require_http_methods(["GET", "POST"])
def payment_create(request, block_id, floor_id, office_id, lease_id):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        lease = get_object_or_404(Lease, pk=lease_id)

        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.lease = lease

            payment.save()  
            return redirect('payment_detail', payment.lease.office.block.pk, payment.lease.office.floor.pk, payment.lease.office.pk, payment.lease.pk, payment.pk)  # Redirect to block detail view

    else:
        blocks = Block.objects.all()
        lease = get_object_or_404(Lease, pk=lease_id)
        payment_form = PaymentForm()

        context = {
            'blocks': blocks,
            'payment_form': payment_form
        }
        return render(request, 'payment/create.html', context)
  
@require_http_methods(["GET", "POST"])
def payment_update(request, block_id, floor_id, office_id, lease_id, pk):
    blocks = Block.objects.all()
    payment = get_object_or_404(Payment, pk=pk)
    lease = get_object_or_404(Lease, pk=lease_id)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST, instance=payment)
        if payment_form.is_valid():
            payment = payment_form.save()
            payment.save()
            return redirect('payment_detail', payment.lease.office.block.pk, payment.lease.office.floor.pk, payment.lease.office.pk, payment.lease.pk, payment.pk)  # Redirect to the detail view
    else:
        payment_form = PaymentForm(instance=payment)
        context = {
            'blocks': blocks,
            'payment': payment,
            'payment_form': payment_form,
        }
    return render(request, 'payment/update.html', context)



def sidebar(request):
  block = Block.objects.all()

  context = {
    'blocks': block,
  }
  return JsonResponse(context)