from setuptools import setup, find_packages


setup(
    name = '{{project}}',
    packages = find_packages(exclude=['tests']),

    python_requires = '>=3.8',
    install_requires = [],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
