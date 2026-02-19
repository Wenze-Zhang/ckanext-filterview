from setuptools import setup, find_packages

setup(
    name="ckanext-filterview",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["ckan"],
    entry_points="""
        [ckan.plugins]
        filterview = ckanext.filterview.plugin:DataTablesView
    """,
)
