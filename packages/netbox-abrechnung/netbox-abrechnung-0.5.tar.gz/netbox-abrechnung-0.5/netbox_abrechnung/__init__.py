from extras.plugins import PluginConfig

class NetBoxAbrechnung(PluginConfig):
    name = 'netbox_abrechnung'
    verbose_name = 'Abrechnung'
    author = "Henrik Hansen"
    author_email = "henrik.hansen@cgi.com"
    description = 'CGI Plugin'
    version = '0.5'
    base_url = 'abrechnung'
    
config = NetBoxAbrechnung
