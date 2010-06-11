from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='zero',
      version=version,
      description="Scheduled task server",
      long_description="""\
      Scheduled task server""",
      classifiers=[],
      keywords='',
      author='Zeomega',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'celery', 'twisted'
      ],
      setup_requires=[
          'setuptools_git',
      ],
      scripts=['zero.tac'],
      entry_points={
          'console_scripts' : ['zerod=zero.zerod:main'],
      }
     )
