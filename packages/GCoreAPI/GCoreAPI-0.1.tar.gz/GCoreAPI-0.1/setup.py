#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='GCoreAPI',
    version='0.1',
    description='Simple GCore API library',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Aleksandr Kuznetsov',
    author_email='amkuznetsov@sberdevices.ru',
    keywords=['gcore', 'gcoreapi'],
    url='https://gitlab.sberdevices.ru/amkuznetsov',
    download_url='https://pypi.org/project/gcoreapi/'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)