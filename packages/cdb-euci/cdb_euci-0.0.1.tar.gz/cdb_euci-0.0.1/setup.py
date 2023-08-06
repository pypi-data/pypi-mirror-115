# -*- coding:utf-8 -*--
import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdb_euci",
    version="0.0.1",
    author="moda",
    author_email="2586935358@qq.com",
    description="CDB Utils By Euci",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=[],
    license='MIT License',
    packages=setuptools.find_packages(),
    platforms=["all"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Natural Language :: Chinese (Simplified)',
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries"
    ],
)
