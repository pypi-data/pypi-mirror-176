"""
      Setup script for flatpy
"""
from setuptools import setup


def long_description():
    """Reads the README.rst file and extracts the portion tagged between
    specific LONG_DESCRIPTION comment lines.
    """
    description = ""
    recording = False
    with open("README.rst") as f:
        for line in f:
            if "END_LONG_DESCRIPTION" in line:
                return description
            elif "LONG_DESCRIPTION" in line:
                recording = True
                continue

            if recording:
                description += line


# Consult here: https://packaging.python.org/tutorials/distributing-packages/
url = "https://github.com/maljovec/flatpy"
setup(
    name="flatpy",
    packages=["flatpy"],
    description="A library for computing samplings in arbitrary dimensions",
    long_description=long_description(),
    test_suite="flatpy.tests",
)
