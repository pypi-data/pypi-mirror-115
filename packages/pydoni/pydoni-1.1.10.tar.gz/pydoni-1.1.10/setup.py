#!/usr/bin/env python

import versioneer
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.in') as requirements_file:
    requirements = requirements_file.read().split()

setup(
    author='Andoni Sooklaris',
    author_email='andoni.sooklaris@gmail.com',
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
        'Programming Language :: Python :: 3.9',
    ],
    description='A Python module for custom-built tools designed and maintained by Andoni Sooklaris.',
    entry_points={
        'console_scripts': [
            'pydoni=pydoni.cli_main:main',
        ],
    },
    install_requires=requirements,
    license='MIT license',
    # long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pydoni',
    name='pydoni',
    packages=find_packages(include=[
                               'pydoni',
                               'pydoni.*',
                           ],
                           exclude=[
                               'tests*',
                               'pydoni/cli/commands/cli_notes.py',
                               'pydoni/cli/app_default_param_values.yaml',
                               'dashboards*',
                           ]),
    setup_requires=[],
    test_suite='tests',
    tests_require=['pytest==6.2.4'],
    url='https://github.com/tsouchlarakis/pydoni',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
)
