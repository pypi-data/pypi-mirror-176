from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='kanwar',
  version='0.0.2',
  description='This is my CMS for FYP in GCS',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kanwar Adnan',
  author_email='kanwaradnanrajput@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='kanwar', 
  packages=find_packages(),
  install_requires=['ttkbootstrap==1.9.0'] 
)