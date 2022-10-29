from setuptools import setup, find_packages

setup(name='downtown-extractor',
      version='0.1.0',
      entry_points={
          'console_scripts': [
              'downtown-extractor = downtown_extractor:main',
          ],
      })

# EOF #
