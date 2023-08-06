from setuptools import setup, find_packages


from os import path
from io import open

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README"), encoding="utf-8") as f:
    long_description = f.read()

setup_kwargs = {
    "name": "v4l2-fix",
    "version": "0.3",
    "license": "GPLv2",
    "requires": [
        "ctypes",
    ],
    "py_modules": [
        "v4l2",
    ],
    "author": "python-v4l2-devel",
    "author_email": "",
    "maintainer": "ArduCam",
    "maintainer_email": "ArduCam <support@arducam.com>",
    "url": "http://pypi.python.org/pypi/v4l2",
    "keywords": "v4l2 video4linux video4linux2 binding ctypes",
    "description": "Python bindings for the v4l2 userspace api.",
    "long_description": long_description,
    "include_package_data": True,
    "use_2to3": True,
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Capture",
    ],
}
setup(**setup_kwargs)
