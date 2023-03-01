from setuptools import setup, find_packages

setup(
    name='CRYPTEX',
    version='0.5.0',
    author='Andrew Sheredko',
    author_email='sheredko.andriy@gmail.com',
    description='CRYPTEX is a web-application which allows user to easily view information about crypto they own and manage their holdings',
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
