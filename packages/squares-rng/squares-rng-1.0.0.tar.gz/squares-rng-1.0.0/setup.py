import os
from setuptools import find_packages, setup

with open('squares/_version.py', 'r') as version_file:
    exec(version_file.read())

with open('README.md', 'r') as readme_file:
    README = readme_file.readlines()

with open('temp_README_DIST.md', 'w') as readme_dist_file:
    for line in README:
        if not line[:25] == '![GitHub Workflow Status]':
            readme_dist_file.write(line)

with open('temp_README_DIST.md', 'r') as readme_dist_file:
    README_DIST = readme_dist_file.read()

setup(
    name='squares-rng',
    version=__version__,
    description='A simple counter-based pseudo random number generator implementation based on arXiv:2004.06278',
    long_description=README_DIST,
    long_description_content_type='text/markdown',
    url='https://github.com/Oafish1/Squares',
    author='Oafish1',
    license='GNLv3',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=['squares'],
    test_suite='tests',
    install_requires=[]
)

os.remove('temp_README_DIST.md')
