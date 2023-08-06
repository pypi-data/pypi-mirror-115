import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="market-client",
    version="0.0.1",
    author="Jan Erik van Woerden",
    author_email="janerik@birds.ai",
    description="Client for the Birds.ai Market server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/janerikvw/market-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)