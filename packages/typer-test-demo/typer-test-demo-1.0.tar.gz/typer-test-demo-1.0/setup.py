from setuptools import setup
import os

# pull long description from README
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name='typer-test-demo',
    version='1.0',
    packages=['cli'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'typer'
    ],
    entry_points='''
        [console_scripts]
        clickctl=cli.main:main
    ''',
)