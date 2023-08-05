from setuptools import setup
import os

VERSION = "1.1.4"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="lofti_gaiaDR2",
    description="lofti_gaiaDR2 is now lofti_gaia",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["lofti_gaia"],
    classifiers=["Development Status :: 7 - Inactive"],
)
