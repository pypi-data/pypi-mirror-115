from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='datelist-sdk-python',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='SDK for https://datelist.io in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    url='https://datelist.io',
    author='Alexis Clarembeau',
    author_email='contact@datelist.io',
    classifiers=[]
)
