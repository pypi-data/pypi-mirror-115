from distutils.core import setup
from setuptools import find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'fileconv',
  packages = find_packages(),
  version = '0.0.1',
  license='MIT',
  description = 'This CLI converts text an MS Word and MS Excel files to PDF files',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'ovanov',
  author_email = 'ovanov@protonmail.com',
  url = 'https://github.com/ovanov/fileconv',
  keywords = ['FITS', 'xml', 'csv', 'CLI programm'],
  platforms='any',
  install_requires=[
          'fpdf >= 1.7.2',
          'pywin31 >= 227',
          'tqdm >= 4.61.2'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  python_requires=">=3.6",
  entry_points={
    'console_scripts': [
      'fileconv=fileconv.cli:main'
    ]
  }
)