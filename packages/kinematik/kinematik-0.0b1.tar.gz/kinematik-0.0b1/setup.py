"""
Kinematik
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kinematik",
    version="0.0b1",
    author="Mackenzie Mathis",
    author_email="mackenzie@post.harvard.edu",
    description="a unicorn in progress",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdaptiveMotorControlLab/kinematik/",
    install_requires=['h5py>=2.7',
                      'ipython~=6.0.0','ipython-genutils==0.2.0','wheel'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
))
