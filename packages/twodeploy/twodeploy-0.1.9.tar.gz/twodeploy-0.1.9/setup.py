from setuptools import setup, find_packages

setup(name='twodeploy',
      version='0.1.9',
      description='Deploying Package',
      # packages = ['twodeploy', 'twodeploy/helpers', 'twodeploy/scripts', 'twodeploy/scripts/shred', 'twodeploy/template', 'twodeploy/template/Build', 'twodeploy/template/Dockerfile', 'twodeploy/template/nginx', 'twodeploy/template/Production',
            # 'twodeploy/template/Build/nextjs',
            # 'twodeploy/template/Build/reactjs',

            # 'twodeploy/template/Dockerfile/nextjs',
            # 'twodeploy/template/Dockerfile/reactjs',

            # 'twodeploy/template/Production/nextjs',
            # 'twodeploy/template/Production/reactjs',

            # 'twodeploy/template/nginx/Dockerfile',
            # 'twodeploy/template/nginx/nginx.conf',
            # 'twodeploy/template/nginx/nginx.sh',
      # ],
      packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
      package_data={'': ['template/**']},
      include_package_data=True,
      install_requires = ["utilum","halo","requests","numpy","pandas","matplotlib"],
      zip_safe = False,
      )
