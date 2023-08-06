from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='easy-cord-python',
  version='1.0.0',
  description='Łatwiejszy bot w pythonie',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='lisior',
  author_email='kox123koz@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='',
  packages=find_packages(),
  install_requires=['Pillow','easy-pil', 'discord.py'] 
)