import os

from setuptools import setup

VERSION = "0.3.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="docker_compose_env",
    description="docker_compose_env is now compile-env",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["compile-env"],
    classifiers=["Development Status :: 7 - Inactive"],
)
