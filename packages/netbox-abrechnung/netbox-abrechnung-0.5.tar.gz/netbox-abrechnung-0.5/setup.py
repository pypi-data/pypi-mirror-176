from setuptools import find_packages, setup

setup(
    name='netbox-abrechnung',
    version='0.5',
    download_url='',
    description='Manage Leistungsscheine in Netbox',
    install_requires=[],
    packages=['netbox_abrechnung','netbox_abrechnung.api','netbox_abrechnung.migrations'],
    include_package_data=True,
    zip_safe=False,
)
