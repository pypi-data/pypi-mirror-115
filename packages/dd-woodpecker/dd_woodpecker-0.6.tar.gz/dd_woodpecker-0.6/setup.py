from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dd_woodpecker',
    packages=['dd_woodpecker'],
    description='A Python library designed to simplify work with the woodpecker API',
    long_description_content_type='text/markdown',
    long_description=long_description,
    version='0.6',
    license='MIT',
    author='DevsData',
    author_email='tpotanski@devsdata.com',
    keywords=['woodpecker', 'woodpecker api', 'devsdata'],
    install_requires=['requests'],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
    ],
)
