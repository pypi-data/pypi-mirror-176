from setuptools import setup

setup(name='twodeploy',
      version='0.1.4',
      description='Deploying Package',
      packages = ['package', 'package/helpers', 'package/nginx', 'package/scripts', 'package/scripts/shred', 'package/template'],
      install_requires = ["utilum","halo","requests","numpy","pandas","matplotlib"],
      zip_safe = False,
      )
