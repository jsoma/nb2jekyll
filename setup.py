#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='nb2jekyll',
      version='0.1dev',
      description='Jekyll-friendly markdown exporter for Jupyter Notebook',
      author='Jonathan Soma',
      author_email='jonathan.soma@gmail.com',
      url='http://www.github.com/jsoma/jupyter-jekyll-converter',
      license='MIT',
      keywords=['jupyter notebook ipython jekyll'],
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      install_requires=['traitlets', 'jupyter'],
        entry_points = {
            'nbconvert.exporters': [
                'jekyll = nb2jekyll:JekyllExporter',
            ],
        }
     )
