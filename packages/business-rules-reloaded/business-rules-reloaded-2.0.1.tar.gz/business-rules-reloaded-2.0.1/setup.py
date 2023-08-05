from setuptools import setup, find_packages

from business_rules.__version__ import __version__ as version

description = (
    "Python DSL for setting up business intelligence rules that can be "
    "configured without code. Based on venmo/business-rules."
)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="business-rules-reloaded",
    version=version,
    author="RonquilloAeon",
    author_email="23411718+RonquilloAeon@users.noreply.github.com",
    url="https://github.com/RonquilloAeon/business-rules",
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7,<4",
)
