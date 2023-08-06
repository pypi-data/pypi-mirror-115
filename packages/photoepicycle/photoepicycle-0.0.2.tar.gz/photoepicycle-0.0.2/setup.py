import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photoepicycle",
    version="0.0.2",
    author="Abdulrahman Binmahfuth",
    author_email="a.binmahfodh@gmail.com",
    description="Represent images using epicycles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abinmahfuth/Picycle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
