from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='HypixelStats',
  version='0.0.1',
  description='This is an API that can be used to get hypixel bedwars and skywars stats.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='',  
  author='Jaishnu',
  author_email='jaishnu.ixi@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='HypixelStats', 
  packages=find_packages(),
  install_requires=['requests'] 
)