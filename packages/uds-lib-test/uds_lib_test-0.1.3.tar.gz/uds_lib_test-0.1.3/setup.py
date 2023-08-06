from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(name='uds_lib_test',
      version='0.1.3',
      description='Lib for UDS API',
      long_description=readme,
      packages=['uds_lib_test'],
      author_email='s@uds.app',
      zip_safe=False)