  
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.9'
]
 
setup(
  name='Square_Numbers',
  version='1.0',
  description='Square of 2 numbers',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pavan',
  author_email='chamarthi.vpk@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='square', 
  packages=find_packages(),
  install_requires=[''] 
)