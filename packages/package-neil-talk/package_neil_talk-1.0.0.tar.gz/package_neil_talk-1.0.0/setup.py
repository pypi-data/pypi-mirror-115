from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='package_neil_talk',
      version='1.0.0',
      description='A small example package',
      long_description=long_description,
      author='neil',
      author_email='xhzhu.nju@gmail.com',
      url='https://xiaohuzhu.xyz',
      install_requires=[],
      license='Apache License',
      packages=find_packages(),
      platforms=['all'],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
      ],
)
