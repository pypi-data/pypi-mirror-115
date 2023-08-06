import pathlib
from setuptools import setup, find_packages

# # The directory containing this file
# HERE = pathlib.Path(__file__).parent

# # The text of the README file
# README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pubsubdil",
    version="0.0.4",
    description="Package for pubsub channel",
    author="DeepInnovations",
    author_email="lidor@deepinnovations.co.uk",
    packages=find_packages(exclude=["tests"]),
    install_requires = ['redis'],
    include_package_data = True
)