from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='ftp_installer',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
         'pyftpdlib==0.7.0',
         'colorama==0.3.2',
         'ftputil==2.6'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
