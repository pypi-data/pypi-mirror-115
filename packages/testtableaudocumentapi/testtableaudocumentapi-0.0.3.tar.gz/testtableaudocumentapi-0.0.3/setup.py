try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='testtableaudocumentapi',
    version='0.0.3',
    author='Avijit',
    author_email='github@tableau.com',
    url='',
    packages=['tableaudocumentapi'],
    license='MIT',
    description='A Python module for working with Tableau files.',
    test_suite='test'
)
