from os import path
from setuptools import setup, find_packages


# """Get the version from the VERSION file"""
with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()


setup(
    name='CRYPTEX',
    version=version,
    author='Andrew Sheredko',
    author_email='sheredko.andriy@gmail.com',
    description='CRYPTEX is a web-application which allows user to easily view information '
                'about crypto they own and manage their holdings',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-migrate',
        'flask-restful',
        'sqlalchemy',
        'jinja2'
    ],
)
