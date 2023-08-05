from setuptools import setup, find_packages
import django_helper

version = django_helper.__version__

with open('README.md', 'r') as f:
    description = f.read()

LONG_DESCRIPTION = description

setup(
    name='django-sca-helper',
    version=version,
    description="A set of useful for Django SCA.",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='helper,library,django',
    author='svtter',
    author_email='hao.xiu@beijing-epoch.com',
    url='https://github.com/svtter/django-sca-helper/',
    license='BSD',
    packages=find_packages(),
    install_requires=['django>=2.1.*'],
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'pytest-django'
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
