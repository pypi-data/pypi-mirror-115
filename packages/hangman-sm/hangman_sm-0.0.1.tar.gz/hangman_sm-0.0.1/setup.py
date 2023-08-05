from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Other Audience',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='hangman_sm',
  version='0.0.1',
  description='a basic game of hangman',
  long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
  url='',  
  author='SM',
  author_email='namefir19@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='hangman,game', 
  packages=find_packages(),
  install_requires=[''] 
)