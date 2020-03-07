from setuptools import setup, find_packages


setup(
    name = 'skel',
    packages = find_packages(exclude=['tests']),

    python_requires = '>=3.8',

    install_requires = [],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],

    scripts = ['scripts/skel'],
)
