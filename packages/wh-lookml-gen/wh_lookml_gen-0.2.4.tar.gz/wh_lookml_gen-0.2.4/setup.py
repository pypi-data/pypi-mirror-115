#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0','lkml==1.1.0'
                'pandas_gbq==0.15.0'
                'pandas==1.3.1'
                'click==8.0.1'
                'GitPython==3.1.18'
                'protobuf==3.17.3'
                'PyYAML==5.4.1'
                'ruamel.base==1.0.0'
            ]

test_requirements = [ ]

setup(
    author="Lewis Baker",
    author_email='lewischarlebaker@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="generates lookml from a warehouse",
    entry_points={
        'console_scripts': [
        'wh_lookml_gen=wh_lookml_gen.cli:lookml',
        'wh_schema_gen=wh_lookml_gen.schema_cli:schema',
        'wh_init_gen=wh_lookml_gen.wh_init_cli:init'
        
        ]
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wh_lookml_gen',
    name='wh_lookml_gen',
    packages=find_packages(include=['wh_lookml_gen', 'wh_lookml_gen.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lewischarlesbaker/wh_lookml_gen',
    version='0.2.4',
    zip_safe=False,
)
