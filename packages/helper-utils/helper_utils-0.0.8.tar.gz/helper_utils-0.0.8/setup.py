from setuptools import setup, find_packages



REQUIREMENTS = ['numpy', 
                'pandas']

setup(
  name='helper_utils',
  version='0.0.8',
  description='Helper functions',
  long_description="Helper functions",
  url='',  
  author='Philipp Friebertshäuser',
  author_email='friebertshaeuser@traide.ai',
  license='MIT', 
  keywords='helper', 
  packages = find_packages(),
  install_requires=REQUIREMENTS
)