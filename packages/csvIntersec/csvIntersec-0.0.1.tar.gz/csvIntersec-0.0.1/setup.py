from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='csvIntersec',
  version='0.0.1',
  description='An Advance CSV Writer and Intersector for @TFM_Hitesh\'s Warehouse Management',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Xeouz',
  author_email='agencyxhq@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='csv', 
  packages=find_packages(),
  install_requires=[] 
)
