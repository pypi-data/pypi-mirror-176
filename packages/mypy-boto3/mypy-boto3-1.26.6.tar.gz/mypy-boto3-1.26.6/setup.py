"""
Setup script for mypy-boto3.
"""
from os.path import abspath, dirname

from setuptools import setup

LONG_DESCRIPTION = open(dirname(abspath(__file__)) + "/README.md", "r").read()


setup(
    name="mypy-boto3",
    version="1.26.6",
    packages=[
        "mypy_boto3",
    ],
    url="https://github.com/youtype/mypy_boto3_builder",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description=(
        "Type annotations for boto3 1.26.6 master module generated with mypy-boto3-builder 7.11.10"
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    keywords=(
        "boto3 type-annotations boto3-stubs mypy mypy-stubs typeshed autocomplete auto-generated"
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://youtype.github.io/boto3_stubs_docs/",
        "Source": "https://github.com/youtype/mypy_boto3_builder",
        "Tracker": "https://github.com/youtype/mypy_boto3_builder/issues",
    },
    install_requires=[
        "boto3",
        "typing-extensions>=4.1.0",
    ],
    package_data={"": ["LICENSE"], "mypy_boto3": ["py.typed"]},
    zip_safe=False,
)
