import os
import sys
from setuptools import setup, find_packages


setup(
    name="ginerator",
    version=0.1,
    description="Description here",
    license="Apache 2.0",
    packages=find_packages(),
    package_data={},
    scripts=[],
    install_requires=["click"],
    extras_require={"test": ["pytest", "pylint!=2.5.0"],},
    entry_points={"console_scripts": ['ginerate = ginerator.ginerator:generate_configs',],},
    classifiers=[],
    tests_require=["pytest"],
    setup_requires=["pytest-runner"],
    keywords="",
)
