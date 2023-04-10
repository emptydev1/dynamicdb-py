from setuptools import setup, find_packages

setup(
    name='dynamicdb',
    version='1.0.0',
    author='emptydev1',
    description='A JSON database made in Python simple and easy to use.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/emptydev1/dynamicdb.py',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dynamicdb = dynamicdb.cli:main'
        ]
    }
)
