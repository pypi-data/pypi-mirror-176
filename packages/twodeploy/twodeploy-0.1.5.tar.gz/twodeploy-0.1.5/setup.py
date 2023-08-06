from setuptools import setup

setup(name='twodeploy',
      version='0.1.5',
      description='Deploying Package',
      packages = ['twodeploy', 'twodeploy/helpers', 'twodeploy/nginx', 'twodeploy/scripts', 'twodeploy/scripts/shred', 'twodeploy/template'],
      install_requires = ["utilum","halo","requests","numpy","pandas","matplotlib"],
      zip_safe = False,
      )
