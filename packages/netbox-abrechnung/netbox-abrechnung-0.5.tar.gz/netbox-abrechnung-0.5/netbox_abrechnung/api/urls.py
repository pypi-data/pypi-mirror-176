from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'netbox_abrechnung'

router = NetBoxRouter()
router.register('kunden', views.KundeViewSet)
router.register('sla', views.SLAViewSet)
router.register('sladevice', views.SLADeviceViewSet)
router.register('slavlan', views.SLAVlanViewSet)

#router.register('contractdevice', views.ContractDeviceViewSet)
#router.register('supplier', views.SupplierViewSet)

urlpatterns = router.urls