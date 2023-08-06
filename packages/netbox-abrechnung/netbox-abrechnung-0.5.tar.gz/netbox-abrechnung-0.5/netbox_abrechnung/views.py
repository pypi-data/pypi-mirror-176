from django.db.models import Count

from netbox.views import generic
from . import filtersets, forms, models, tables
from .models import SLA, Kunde, SLADevice, SLAVlan

# #
# #  Leistungsscheinvlan views
# #

class SLAVlanView(generic.ObjectView):
    queryset = models.SLAVlan.objects.all()

class SLAVlanListView(generic.ObjectListView):
    queryset = models.SLAVlan.objects.annotate(
    )
    
    filterset = filtersets.DeviceFilterSet
    filterset_form = forms.SLAVlanFilterForm
    table = tables.SLAVlanTable

class SLAVlanEditView(generic.ObjectEditView):
    queryset = models.SLAVlan.objects.all()
    form = forms.SLAVlanForm

class SLAVlanDeleteView(generic.ObjectDeleteView):
    queryset = models.SLAVlan.objects.all()

# #
# # Leistungsscheindevice views
# #

class SLADeviceView(generic.ObjectView):
    queryset = models.SLADevice.objects.all()

class SLADeviceListView(generic.ObjectListView):
    queryset = models.SLADevice.objects.annotate(
    )
    
    filterset = filtersets.DeviceFilterSet
    filterset_form = forms.SLADeviceFilterForm
    table = tables.SLADeviceTable

class SLADeviceEditView(generic.ObjectEditView):
    queryset = models.SLADevice.objects.all()
    form = forms.SLADeviceForm

class SLADeviceDeleteView(generic.ObjectDeleteView):
    queryset = models.SLADevice.objects.all()

# #
# # Leistungsschein views
# #

class SLAView(generic.ObjectView):
    queryset = models.SLA.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.SLADeviceTable(instance.devices.all())
        table.configure(request)

        vlan = tables.SLAVlanTable(instance.vlans.all())
        vlan.configure(request)

        return {
            'device_table': table,
            'vlan_table': vlan,
        }

class SLAListView(generic.ObjectListView):
    queryset = models.SLA.objects.annotate(
      device_count=Count('devices'),
      vlan_count=Count('vlans')
    )
    filterset = filtersets.SLAFilterSet
    filterset_form = forms.SLAFilterForm
    table = tables.SLATable

class SLAEditView(generic.ObjectEditView):
    queryset = models.SLA.objects.all()
    form = forms.SLAForm

class SLADeleteView(generic.ObjectDeleteView):
    queryset = models.SLA.objects.all()

class SLABulkImportView(generic.BulkImportView):
    queryset = models.SLA.objects.all()
    model_form = forms.SLACSVForm
    table = tables.SLATable

class SLABulkEditView(generic.BulkEditView):
    queryset = models.SLA.objects.all()
    table = tables.SLATable
    form = forms.SLABulkEditForm
    filterset = filtersets.SLAFilterSet

class SLABulkDeleteView(generic.BulkDeleteView):
    queryset = models.SLA.objects.all()
    table = tables.SLATable

# #
# # Kunde views
# #

class KundeView(generic.ObjectView):
    queryset = models.Kunde.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.SLATable(instance.kunden.all())
        table.configure(request)
        return {
            'sla_table': table,
        }

class KundeListView(generic.ObjectListView):
    filterset = filtersets.KundeFilterSet
    filterset_form = forms.KundeFilterForm

    queryset = models.Kunde.objects.annotate(
        sla_count=Count('kunden')
    )
    table = tables.KundeTable

class KundeEditView(generic.ObjectEditView):
    queryset = models.Kunde.objects.all()
    form = forms.KundeForm

class KundeDeleteView(generic.ObjectDeleteView):
    queryset = models.Kunde.objects.all()

class KundeBulkImportView(generic.BulkImportView):
    queryset = models.Kunde.objects.all()
    model_form = forms.KundeCSVForm
    table = tables.KundeTable


