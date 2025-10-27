# setup.py
from setuptools import setup, find_packages

setup(
    name='django-emailer',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'python-decouple>=3.6',
        'python-dotenv>=1.2',
        'requests>=2.25',
    ],
    description='Reusable Django email backend for ZeptoMail',
    author='Hariri A.',
    author_email='hariri.bin.abdullah@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)