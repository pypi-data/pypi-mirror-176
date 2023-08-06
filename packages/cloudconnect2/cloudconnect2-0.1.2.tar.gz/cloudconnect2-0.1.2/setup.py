from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='cloudconnect2',
    packages=find_packages(include=['cloudconnect2']),
    version='0.1.2',
    description='A package to connect retrieve the API credentials in SAP BTP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joel Kischkel',
    author_email='joel.kischkel@syntax.com',
    license='MIT',
    install_requires=['requests', 'cfenv'],
)

