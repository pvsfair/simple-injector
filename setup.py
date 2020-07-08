import pathlib
import os
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

NAME = "simple-injector"
about = {}
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(HERE, project_slug, '__version__.py')) as f:
    exec(f.read(), about)

# This call to setup() does all the work
setup(
    name=NAME,
    version=about['__version__'],
    description="Dependency Injection made simple.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pvsfair/simple-injector",
    author="Paulo Victor Alvares",
    author_email="pvsfair@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
)
