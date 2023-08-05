from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cm-feet_conversion',
  version='0.0.1',
  description='A very basic package to convert height measurement from cm to feet and viceversa',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Bijay Adhikari',
  author_email='bjsharma555@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='measurement', 
  packages=find_packages(),
  install_requires=[''] 
)
