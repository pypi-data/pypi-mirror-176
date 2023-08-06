import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()
    long_description = README

setup(
    name='Flask-Scheduler',
    version='0.0.5',
    url='https://github.com/furqonat/flask-scheduler',
    license='MIT',
    author='Furqon Romdhani',
    author_email='danixml31@gmail.com',
    description='Background scheduler for Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['flask_scheduler'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['Flask', 'apscheduler'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_scheduler'
)
