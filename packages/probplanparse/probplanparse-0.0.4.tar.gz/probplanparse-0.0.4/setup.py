from setuptools import setup, find_packages


setup(
  name='probplanparse',
  version='0.0.4',
  description='Parse report from prob plan in ext planner',
  long_description='# PR Result \n A small library that parses through the report.txt file and converts to a `user-dict` made up of Hypothesis objects. This will use report.txt files from the `external-project`. \n Use `pip install pr-result` to install package.',
  url='',
  author='Tomo Bessho',
  author_email='tomobessho018@gmail.com',
  packages=find_packages(),
  install_requires=['wheel']
)