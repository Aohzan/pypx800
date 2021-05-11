import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypx800",
    version="2.2.0",
    author="Aohzan",
    author_email="aohzan@gmail.com",
    description="Control the IPX800 and some of its extensions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aohzan/pypx800",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
