from django import forms

from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm,NetBoxModelCSVForm,NetBoxModelBulkEditForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from utilities.forms import CSVModelChoiceField
from .models import *
from dcim.models import Device
from ipam.models import VLAN
from . import models, views

class SLAVlanFilterForm(NetBoxModelFilterSetForm):
    model = SLAVlan

    sla = forms.ModelMultipleChoiceField(
        queryset=SLAVlan.objects.all(),
        required=False
    )

class SLAVlanForm(NetBoxModelForm):
    kunde = DynamicModelChoiceField(
        queryset=Kunde.objects.all(),
        required=False
    )

    sla = DynamicModelChoiceField(
        queryset=SLA.objects.all(),
        query_params={
            'kunde': '$kunde'
        }
    )
    vlan = DynamicModelChoiceField(
        queryset=VLAN.objects.all()
    )

    class Meta:
        model = SLADevice
        fields = ('kunde','sla','vlan')


class SLADeviceFilterForm(NetBoxModelFilterSetForm):
    model = SLADevice

    sla = forms.ModelMultipleChoiceField(
        queryset=SLADevice.objects.all(),
        required=False
    )

class SLADeviceForm(NetBoxModelForm):
    kunde = DynamicModelChoiceField(
        queryset=Kunde.objects.all(),
        required=False
    )

    sla = DynamicModelChoiceField(
        queryset=SLA.objects.all(),
        query_params={
            'kunde': '$kunde'
        }
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all()
    )

    class Meta:
        model = SLADevice
        fields = ('kunde','sla','device')

class SLAForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = SLA
        fields = ('name','kunde','comments')

class SLAFilterForm(NetBoxModelFilterSetForm):
    model = SLA
    
    kunde = forms.ModelMultipleChoiceField(
        queryset=Kunde.objects.all(),
        required=False
    )

class SLABulkEditForm(NetBoxModelBulkEditForm):
    model = SLA
    pk = forms.ModelMultipleChoiceField(
        queryset=SLA.objects.all(),
        widget=forms.MultipleHiddenInput
    )

class SLACSVForm(NetBoxModelCSVForm):
    name = forms.CharField(
        required=True
    )

    kunde = CSVModelChoiceField(
        queryset=Kunde.objects.all(),
        required=True,
        to_field_name="name",
        help_text="name of LS Kunde not found.",
        error_messages={
            "invalid_choice": "Kunde not found.",
        }
    )


    class Meta:
        model = SLA
        fields = ('name','kunde')


class KundeForm(NetBoxModelForm):
    class Meta:
        model = Kunde
        fields = ('name',)


class KundeCSVForm(NetBoxModelCSVForm):
    class Meta:
        model = Kunde
        fields = (
            "name",
        )

class KundeFilterForm(NetBoxModelFilterSetForm):
    model = Kunde