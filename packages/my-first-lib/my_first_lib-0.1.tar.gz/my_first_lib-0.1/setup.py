from setuptools import setup, find_packages

setup(
    name='my_first_lib',
    version = '0.1',
    author = 'me',
    author_email = 'some@email.com',
    description = 'This  is very useful package',
    long_description = open('README.md').read(),
    packages = find_packages()
)