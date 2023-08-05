import setuptools
from pr2apisdk import version

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pr2apisdk",
    version=version,
    author="pr2apisdk",
    author_email="pr2apisdk@outlook.com",
    description="Api Sdk For Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pr2apisdk/pr2apisdk_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        ##"Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
