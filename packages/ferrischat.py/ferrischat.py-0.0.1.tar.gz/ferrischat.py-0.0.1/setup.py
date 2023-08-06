from setuptools import setup
import re

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="ferrischat.py",
    author='Cryptex',
    url="https://pypi.org/project/ferrispy",
    version='0.0.1',
    packages=[],
    license="MIT",
    description="This is a mirror package of ferrispy please install that package instead.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['ferrispy'],
)
