import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="constlib",
    version="0.1.0",
    author="Micfong",
    author_email="micfong2@outlook.com",
    description="A powerful constant library for scientific computing with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0Micfong0/constlib",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    ],
)
