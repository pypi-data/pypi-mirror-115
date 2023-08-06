import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="countre",
    version="0.0.4",
    author="Matthew Barnes",
    author_email="mwt.barnes@outlook.com",
    description="Package to get country data from country names.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwtb47/countre",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
