from distutils.core import setup


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()
    print(long_description)

setup(
  name='dd_woodpecker',
  packages=['dd_woodpecker'],
  version='0.2',
  license='MIT',
  description='A Python library designed to simplify work with the woodpecker API',
  long_description=long_description,
  long_description_content_type="text/markdown",
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