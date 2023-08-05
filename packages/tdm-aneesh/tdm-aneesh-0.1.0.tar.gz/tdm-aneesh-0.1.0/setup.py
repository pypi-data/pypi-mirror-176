from setuptools import setup

setup(
   name='achakra',
   version='1.0.0',
   description='A useful module',
   author='Aneesh Chakravarthula',
   author_email='srianeesh328@gmail.com',
   packages=['achakra'],  #same as name
   install_requires=['wheel', 'bar'], #external packages as dependencies
)