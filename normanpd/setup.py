#Setup file for installing noramnpd_arrest database
#https://marthall.github.io/blog/how-to-package-a-python-app/

from setuptools import setup, find_packages

setup(
    name='Activity Police Report Extraction',    # This is the name of your PyPI-package
    version='1.0',                          # Update the version number for new releases
    author = 'Umesh Sai Gurram',
    author_email = 'umeshsai34@ou.edu',
    packages = find_packages()
    )
