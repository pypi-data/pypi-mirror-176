from setuptools import setup, find_packages

setup(name='twodeploy',
      version='0.1.12',
      description='Deploying Package',
      packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
      # package_data={'': ['template/**']},
      # include_package_data=True,
      install_requires = ["utilum","halo","requests","numpy","pandas","matplotlib"],
      zip_safe = False,
      )
