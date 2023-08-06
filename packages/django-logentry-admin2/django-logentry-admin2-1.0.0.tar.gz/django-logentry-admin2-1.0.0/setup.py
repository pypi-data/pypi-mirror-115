from setuptools import setup

setup(
    name='django-logentry-admin2',
    author='Yuri Prezument',
    author_email='y@yprez.com',
    version='1.0.0',
    packages=['logentry_admin'],
    package_data={
        'logentry_admin': [
            '*.po',
        ],
    },
    include_package_data=True,
    license='ISC',
    url='https://github.com/yprez/django-logentry-admin',
    description='Show all LogEntry objects in the Django admin site.',
    install_requires=[
        'Django>=3.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
