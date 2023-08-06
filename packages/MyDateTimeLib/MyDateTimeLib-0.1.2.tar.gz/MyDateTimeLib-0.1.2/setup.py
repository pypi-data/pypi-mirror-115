from setuptools import find_packages, setup


setup(
    name='MyDateTimeLib',
    packages=find_packages(include=['MyDateTimeLib']),
    version='0.1.2',
    description='Date time from string library',
    author='Praveen Kumar Srivas',
    license='MIT',
    install_requires=['datefinder'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==5.3.1'],
    test_suite='tests',
)