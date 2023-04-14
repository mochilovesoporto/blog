from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)

#packages tells python what package directories to include
# find_packages() finds these directories automatically
# include_package_data used to inlude static & template directories
# Manifest.in tells  used to tell what this other data is