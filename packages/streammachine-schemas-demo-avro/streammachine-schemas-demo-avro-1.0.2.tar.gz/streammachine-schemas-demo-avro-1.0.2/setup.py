#!/usr/bin/env python
from setuptools import setup, find_packages

top_package = "streammachine_io_streammachine_schemas_demo_v1"

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Stream Machine B.V.",
    author_email='apis@streammachine.io',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    description="Python classes for demo",
    install_requires=[
        "streammachine-schemas-common==1.0.0",
        "avro-gen==0.3.0",
        "tzlocal==2.1"
        # avro-gen has no restriction on tzlocal version and requires .localize() which is not present in the 3.x rewrite of tzlocal
    ],
    long_description=readme,
    include_package_data=True,
    keywords='streammachine api client driver schema',
    name='streammachine-schemas-demo-avro',
    packages=find_packages(),
    package_data={top_package: ['schema.avsc']},
    setup_requires=[],
    version='1.0.2',
    zip_safe=False,
)
