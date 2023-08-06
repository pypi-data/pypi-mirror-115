from setuptools import setup, find_packages

setup(
    name='django-grappelli-extensions2',
    version='1.0.2',
    url='http://github.com/django-grappelli-extensions/django-grappelli-extensions',
    author='Paulo R. Macedo, Igor P. Leroy',
    author_email='proberto.macedo@gmail.com, ip.leroy@gmail.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    description='Extensions for Grappelli Admin interface',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
    install_requires=['django', 'django-grappelli', 'django-classy-tags'],
    package_data={'grappelli_extensions': [
        'templates/admin/includes_grappelli/*.html',
        'templates/grappelli/*.html'
        'static/grappelli_extensions/css/*.css',
    ]},
)
