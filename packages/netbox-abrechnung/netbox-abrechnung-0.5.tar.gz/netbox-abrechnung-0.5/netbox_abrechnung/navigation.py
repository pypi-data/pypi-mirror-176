from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_abrechnung:kunde_list',
        link_text='Customers',
        buttons= [PluginMenuButton(
            link='plugins:netbox_abrechnung:kunde_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_abrechnung.add_kunde"],
        )
        ,
        PluginMenuButton(
                "plugins:netbox_abrechnung:kunde_import",
                "Import",
                "mdi mdi-upload",
                ButtonColorChoices.CYAN,
                permissions=["netbox_abrechnung.add_kunde"],
            )
        ],
        permissions=["netbox_abrechnung.view_kunde"],
    ),
    PluginMenuItem(
        link='plugins:netbox_abrechnung:sla_list',
        link_text='SLAs',
        buttons= [
        PluginMenuButton(
            link='plugins:netbox_abrechnung:sla_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_abrechnung.add_sla"],
        )        
        ,
        PluginMenuButton(
                "plugins:netbox_abrechnung:sla_import",
                "Import",
                "mdi mdi-upload",
                ButtonColorChoices.CYAN,
                permissions=["netbox_abrechnung.add_sla"],
            )
        ],
        permissions=["netbox_abrechnung.view_sla"],
    ),
PluginMenuItem(
        link='plugins:netbox_abrechnung:sladevice_list',
        link_text='Devices',
        buttons= [
        PluginMenuButton(
            link='plugins:netbox_abrechnung:sladevice_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_abrechnung.add_sladevice"],
        )],
        permissions=["netbox_abrechnung.view_sladevice"],
    ),
PluginMenuItem(
        link='plugins:netbox_abrechnung:slavlan_list',
        link_text='Vlans',
        buttons= [
        PluginMenuButton(
            link='plugins:netbox_abrechnung:slavlan_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_abrechnung.add_sladevice"],
        )],
        permissions=["netbox_abrechnung.view_sladevice"],
    ),
    
)
