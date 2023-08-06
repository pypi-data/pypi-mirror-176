# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Jung Song",
    description="A package for utils",
    name="essexpropds",
    packages=find_packages(include=["essexpropds", "essexpropds.*"]),
    version="0.0.4",
)
