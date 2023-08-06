from distutils.core import setup
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'ran2', 
  packages = ['ran2'],
  version = '1.2',     
  license='MIT',  
  description = 'Implements the ran2 function from FORTRAN Numerical Recipes',
  long_description = long_description,
  author = 'Drake Gates',            
  author_email = 'dgates8@gmail.com',
  keywords = ['random', 'number', 'generator', 'numerical recipes', 'rng'],
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)