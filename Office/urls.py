from django.urls import path
from .views import (dashboard_view, 
                    block_create, block_detail, block_update, 
                    floor_detail, floor_create, floor_update,
                    office_detail, office_create, office_update,
                    lease_detail, lease_create, lease_update,
                    payment_detail, payment_create, payment_update,
                    sidebar)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    #Block
    path('block/<int:pk>/', block_detail, name='block_detail'),
    path('block/create/', block_create, name='block_create'),
    path('block/<int:pk>/edit/', block_update, name='block_update'),
    #Floor
    path('block/<int:block_id>/floor/<int:pk>/', floor_detail, name='floor_detail'),
    path('block/<int:block_id>/floor/create/', floor_create, name='floor_create'),
    path('block/<int:block_id>/floor/<int:pk>/edit/', floor_update, name='floor_update'),
    #Floor
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:pk>', office_detail, name='office_detail'),
    path('block/<int:block_id>/floor/<int:floor_id>/office/create/', office_create, name='office_create'),
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:pk>/edit/', office_update, name='office_update'),
    #Lease
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:office_id>/lease/<int:pk>/', lease_detail, name='lease_detail'),
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:office_id>/lease/create/', lease_create, name='lease_create'),
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:office_id>/lease/<int:pk>/edit/', lease_update, name='lease_update'),
    #Payment
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:office_id>/lease/<int:lease_id>/payment/<int:pk>/', payment_detail, name='payment_detail'),
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:office_id>/lease/<int:lease_id>/payment/create/', payment_create, name='payment_create'),
    path('block/<int:block_id>/floor/<int:floor_id>/office/<int:office_id>/lease/<int:lease_id>/payment/<int:pk>/edit/', payment_update, name='payment_update'),

    path('api/sidebar', sidebar, name='sidebar-data'),
]

