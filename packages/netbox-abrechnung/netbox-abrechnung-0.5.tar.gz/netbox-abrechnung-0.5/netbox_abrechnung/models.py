from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from datetime import datetime, date

from netbox.models import NetBoxModel

class Kunde(NetBoxModel):

    name = models.CharField(
        max_length=100,
        help_text="Name des Kunden",
        unique=True
    )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_abrechnung:kunde', args=[self.pk])

    class Meta:
        ordering = ('name',)

class SLA(NetBoxModel):
    name = models.CharField(
        max_length=100,
        help_text="Name des Leistungsschein",
    )

    kunde = models.ForeignKey(
        to=Kunde, 
        on_delete=models.PROTECT,
        related_name='kunden',
    )

    def __str__(self):
        return f'{self.kunde.name} - {self.name}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_abrechnung:sla', args=[self.pk])

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'kunde')
        
class SLADevice(NetBoxModel):
    device = models.OneToOneField(
        to="dcim.Device", 
        on_delete=models.CASCADE, 
    )
   
    sla = models.ForeignKey(
        to=SLA, 
        on_delete=models.PROTECT,
        related_name='devices',
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.device}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_abrechnung:sladevice', args=[self.pk])


class SLAVlan(NetBoxModel):
    vlan = models.OneToOneField(
        to="ipam.Vlan", 
        on_delete=models.CASCADE, 
    )
   
    sla = models.ForeignKey(
        to=SLA, 
        on_delete=models.PROTECT,
        related_name='vlans',
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.vlan}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_abrechnung:slavlan', args=[self.pk])