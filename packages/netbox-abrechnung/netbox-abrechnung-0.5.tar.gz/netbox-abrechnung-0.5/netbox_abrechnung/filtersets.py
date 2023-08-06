import django_filters
from django.db.models import Q

from extras.filtersets import LocalConfigContextFilterSet
from netbox.filtersets import NetBoxModelFilterSet
from .models import *

class DeviceFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLADevice
        fields = ('id','sla','device',)

class SLAFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SLA
        fields = ('id','kunde',)

class KundeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Kunde
        fields = ('id','name',)

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
        