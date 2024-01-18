from setuptools import setup, find_packages
from gicha.version import get_version


def get_long_description():
    with open("README.md", "r") as readme:
        return readme.read()


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="gicha",
    version=get_version(),
    description="Operating Chalice from Github",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="HEI",
    author_email="contact@hei.school",
    url="https://github.com/hei-school/gicha-cli",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=required,
)
