from setuptools import setup, find_packages

setup(name='twodeploy',
      version='0.1.8',
      description='Deploying Package',
      # packages = ['twodeploy', 'twodeploy/helpers', 'twodeploy/scripts', 'twodeploy/scripts/shred', 'twodeploy/template', 'twodeploy/template/Build', 'twodeploy/template/Dockerfile', 'twodeploy/template/nginx', 'twodeploy/template/Production'],
      packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
      package_data={'': ['license.txt']},
      include_package_data=True,
      install_requires = ["utilum","halo","requests","numpy","pandas","matplotlib"],
      zip_safe = False,
      )
