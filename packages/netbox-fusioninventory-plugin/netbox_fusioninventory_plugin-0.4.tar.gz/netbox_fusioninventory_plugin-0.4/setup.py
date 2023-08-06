from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name='netbox_fusioninventory_plugin',
    version='0.4',
    description='A Plugin for import devices from fusion inventory agent',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/Milka64/netbox-fusioninventory-plugin',
    author='Michael Ricart',
    license='BSD License',
    install_requires=[
        'bs4',
        'lxml',
        ],
    packages=find_packages(),
    include_package_data=True,
)

