from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='DatetimeRsys01',
  version='0.0.2',
  description='Python Library for DATE TIME finder from a String',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Praveen Kumar Srivas',
  author_email='pks101295nit2017@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='date time', 
  packages=find_packages(),
  install_requires=['regex','datefinder'] 
)