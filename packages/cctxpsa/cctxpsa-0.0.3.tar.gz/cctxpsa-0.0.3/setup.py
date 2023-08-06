# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = '0.0.3'

setup(name='cctxpsa',
      version=VERSION,
      description="A command line tool for CCTX to analyser pcap and compare with CCTX's observables offline",
      long_description='',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python cctx pcap cctxpa terminal',
      author='zoeyyy',
      author_email='yzou10@uoguelph.ca',
      url='https://github.com/zoeyyyzou/cctx-pcap-safe-analyser',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'dpkt',
          'progress',
          'requests',
          'rich',
          'scalable-cuckoo-filter',
          'sklearn',
      ],
      entry_points={
          'console_scripts': [
              'cctxpsa = cctxpsa.cctxpsa:main'
          ]
      },
      )
