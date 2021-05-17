from distutils.core import setup
from setuptools import setup

setup(name='chia_mgr',
      author='Alberto Treto',
      author_email='albertotreto@gmail.com',
      version='1.0',
      install_requires=['pandas','psutil'],
      entry_points={
                  'console_scripts': [
                      'main=main:main',
                  ],
            },
      project_urls={
                'Source': 'https://github.com/atretolopez/chia_mgr',
            },
)