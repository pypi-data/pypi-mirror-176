#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    "requests",
    "dacite"
 ]

test_requirements = [
    "requests",
    "dacite"
 ]

setup(
    author="Ollez95",
    author_email='gustalorena@hotmail.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="First version of Python Wrapper TMDB API",
    install_requires=requirements,
    license="MIT license",
    long_description="Python Wrapper TMDB API where you can query the version 3 of this api.",
    include_package_data=True,
    keywords=["tmdb_wrapper","python","requests","dacite"],
    name='tmdb_wrapper',
    packages=find_packages(include=['tmdb_wrapper', 'tmdb_wrapper.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Ollez95/tmdb_wrapper',
    version='0.4.0',
    zip_safe=False,
)
