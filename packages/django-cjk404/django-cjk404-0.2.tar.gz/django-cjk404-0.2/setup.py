from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="django-cjk404",
    description="django-cjk404 is now wagtail-cjk404",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["wagtail-cjk404"],
    classifiers=["Development Status :: 7 - Inactive"],
)
