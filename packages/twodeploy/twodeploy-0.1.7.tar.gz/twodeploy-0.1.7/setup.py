from setuptools import setup

setup(name='twodeploy',
      version='0.1.7',
      description='Deploying Package',
      packages = ['twodeploy', 'twodeploy/helpers', 'twodeploy/scripts', 'twodeploy/scripts/shred', 'twodeploy/template', 'twodeploy/template/Build', 'twodeploy/template/Dockerfile', 'twodeploy/template/nginx', 'twodeploy/template/Production'],
      install_requires = ["utilum","halo","requests","numpy","pandas","matplotlib"],
      zip_safe = False,
      )
