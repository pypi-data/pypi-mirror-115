from distutils.core import setup

setup(
  name='dd_woodpecker',
  packages=['dd_woodpecker'],
  version='0.1',
  license='MIT',
  description='A Python library designed to simplify work with the woodpecker API',
  author='DevsData',
  author_email='tpotanski@devsdata.com',
  url='',
  download_url='',
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