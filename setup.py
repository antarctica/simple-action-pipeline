import setuptools

setuptools.setup(
  include_package_data=True,
  name='sap',
  version='0.0.1',
  description='simple action pipeline python package',
  author='matscorse',
  author_email='matsco@bas.ac.uk',
  packages=setuptools.find_packages(),
  install_requires=['jug', 'pytest'],
  long_description=get_content("README.md"),
  long_description_content_type="text/markdown",
  url="https://www.github.com/antarctica",
  classifiers=[el.lstrip() for el in """Development Status :: 3 - Alpha
    Intended Audience :: Science/Research
    Intended Audience :: System Administrators
    License :: OSI Approved :: MIT License
    Natural Language :: English
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 3
    Topic :: Scientific/Engineering""".split('\n')],
)
