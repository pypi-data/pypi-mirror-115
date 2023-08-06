# -*- coding: utf-8 -*-
"""Installer for the collective.googlecloudlogging package."""

from setuptools import find_packages, setup

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.googlecloudlogging',
    version='1.0',
    description="Google Cloud Logging Integration",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Peter Holzer',
    author_email='peter.holzer@agitator.com',
    url='https://github.com/collective/collective.googlecloudlogging',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.googlecloudlogging',
        'Source': 'https://github.com/collective/collective.googlecloudlogging',
        'Tracker': 'https://github.com/collective/collective.googlecloudlogging/issues',
        # 'Documentation': 'https://collective.googlecloudlogging.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        "google-cloud-logging"
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    """,
)
