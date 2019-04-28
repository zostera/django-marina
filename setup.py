import os

from setuptools import find_packages, setup

import re

VERSIONFILE = "src/marina/_version.py"
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"

try:
    __version__ = re.search(VSRE, open(VERSIONFILE, "rt").read(), re.M).group(1)
except:  # noqa
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="django-marina",
    zip_safe=False,  # eggs are the devil.
    version=__version__,
    description="Reusable Django extensions by Zostera.",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    author="Dylan Verheul",
    author_email="dylan@zostera.nl",
    url="https://github.com/zostera/django-marina/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    python_requires=">=3.4",
    install_requires=["Django>=2,<3.0"],
    test_suite="runtests",
)
