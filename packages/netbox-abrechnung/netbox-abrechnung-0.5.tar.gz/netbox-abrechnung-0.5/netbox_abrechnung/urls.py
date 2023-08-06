from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views

urlpatterns = (

#    # Supplier
#     path('supplier/', views.SupplierListView.as_view(), name='supplier_list'),
#     path('supplier/add/', views.SupplierEditView.as_view(), name='supplier_add'),
#     path('supplier/<int:pk>/', views.SupplierView.as_view(), name='supplier'),
#     path('supplier/<int:pk>/edit/', views.SupplierEditView.as_view(), name='supplier_edit'),
#     path('supplier/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
#     path('supplier/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='supplier_changelog', kwargs={ 'model': models.Supplier}),

# Kunden    
    path('kunde/', views.KundeListView.as_view(), name='kunde_list'),
    path('kunde/add/', views.KundeEditView.as_view(), name='kunde_add'),
    path("kunde/import/", views.KundeBulkImportView.as_view(), name="kunde_import"),
    path('kunde/<int:pk>/', views.KundeView.as_view(), name='kunde'),
    path('kunde/<int:pk>/edit/', views.KundeEditView.as_view(), name='kunde_edit'),
    path('kunde/<int:pk>/delete/', views.KundeDeleteView.as_view(), name='kunde_delete'),
    path('kunde/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='kunde_changelog', kwargs={ 'model': models.Kunde}),


# Leistungsschein    
    path('sla/', views.SLAListView.as_view(), name='sla_list'),
    path('sla/add/', views.SLAEditView.as_view(), name='sla_add'),
    path('sla/edit/', views.SLABulkEditView.as_view(), name='sla_bulk_edit'),
    path('sla/delete/', views.SLABulkDeleteView.as_view(), name='sla_bulk_delete'),
    path("sla/import/", views.SLABulkImportView.as_view(), name="sla_import"),
    path('sla/<int:pk>/', views.SLAView.as_view(), name='sla'),
    path('sla/<int:pk>/edit/', views.SLAEditView.as_view(), name='sla_edit'),
    path('sla/<int:pk>/delete/', views.SLADeleteView.as_view(), name='sla_delete'),
    path('sla/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='sla_changelog', kwargs={ 'model': models.SLA}),

# LeistungsscheinDevice    
    path('sladevice/', views.SLADeviceListView.as_view(), name='sladevice_list'),
    path('sladevice/add/', views.SLADeviceEditView.as_view(), name='sladevice_add'),
    path('sladevice/<int:pk>/', views.SLADeviceView.as_view(), name='sladevice'),
    path('sladevice/<int:pk>/edit/', views.SLADeviceEditView.as_view(), name='sladevice_edit'),
    path('sladevice/<int:pk>/delete/', views.SLADeviceDeleteView.as_view(), name='sladevice_delete'),
    path('sladevice/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='sladevice_changelog', kwargs={ 'model': models.SLADevice}),

# LeistungsscheinVlan
    path('slavlan/', views.SLAVlanListView.as_view(), name='slavlan_list'),
    path('slavlan/add/', views.SLAVlanEditView.as_view(), name='slavlan_add'),
    path('slavlan/<int:pk>/', views.SLAVlanView.as_view(), name='slavlan'),
    path('slavlan/<int:pk>/edit/', views.SLAVlanEditView.as_view(), name='slavlan_edit'),
    path('slavlan/<int:pk>/delete/', views.SLAVlanDeleteView.as_view(), name='slavlan_delete'),
    path('slavlan/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='slavlan_changelog', kwargs={ 'model': models.SLADevice}),


)