from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = "Upload Packages to PiPy easier and faster than ever before"
LONG_DESCRIPTION = "A Package that allows you to upload to pip via 'python3 -m PPP -f (filename_to_upload)'"

# Setting up
setup(
    name="pip_package_poster",
    version=VERSION,
    author="JartC0ding (Moritz Schittenhelm)",
    author_email="moritz5911@gmail.com",
    description=DESCRIPTION,
    long_description_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["twine"],
    keywords=["python", "pip", "PiPy", "post", "easy"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X"
    ]
)