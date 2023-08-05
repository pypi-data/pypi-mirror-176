from setuptools import setup,   find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package-test-calculator",
    version="0.0.1",
    author="VitorFran1337",
    author_email="vitor.pereira0437@gmail.com",
    description="test package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VitorFran1337/package-test-calculator",
    package=find_packages(),
    python_requires='>=3.0',
)
