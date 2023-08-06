from netbox_abrechnung.views import SLAVlanListView
from rest_framework import serializers
from ipam.api.serializers import NestedPrefixSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Kunde, SLA, SLADevice, SLAVlan
from dcim.api.nested_serializers import NestedDeviceSerializer

# class ContractSerializer(NetBoxModelSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name='plugins-api:netbox_maintenancecontract_plugin-api:contract-detail'
#     )

#     class Meta:
#         model = Contract
#         fields = (
#             'id', 'url','display',
#             'status', 'supplier', 'description', 'contract_number', 'start_of_contract', 'end_of_contract', 'status', 'comments',
#             'custom_fields', 'created',
#             'last_updated',
#         )

# class ContractDeviceSerializer(NetBoxModelSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name='plugins-api:netbox_maintenancecontract_plugin-api:contractdevice-detail'
#     )

#     class Meta:
#         model = ContractDevice
#         fields = (
#             'id', 'url','pk','display',
#             'device','contract',
#             'custom_fields', 'created',
#             'last_updated',
#         )

class SLAVlanSerializer(NetBoxModelSerializer):
    vlan = NestedDeviceSerializer(
        many=False,
        read_only=False,
        required=True,
        help_text="Vlan",
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_abrechnung-api:sla-detail'
    )

    class Meta:
        model = SLAVlan
        fields = (
        'id', 'url','display', 
        "vlan", "sla",
        )

class SLADeviceSerializer(NetBoxModelSerializer):
    device = NestedDeviceSerializer(
        many=False,
        read_only=False,
        required=True,
        help_text="Device",
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_abrechnung-api:sladevice-detail'
    )

    class Meta:
        model = SLADevice
        fields = (
        'id', 'url','display', 
        "device", "sla",
        )



class SLASerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_abrechnung-api:sla-detail'
    )

    class Meta:
        model = SLA
        fields = (
        'id', 'url','pk', 'display',
        "name", "kunde",
        )


class KundeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_abrechnung-api:kunde-detail'
    )

    class Meta:
        model = Kunde
        fields = (
        'id', 'url','pk', 'display',
        "name",
        )

