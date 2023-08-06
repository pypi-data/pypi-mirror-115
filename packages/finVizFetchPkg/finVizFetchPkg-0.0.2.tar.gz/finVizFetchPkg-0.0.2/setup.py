import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finVizFetchPkg",
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="A package to fetch finViz data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p-hiroshige/finVizFetch.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)