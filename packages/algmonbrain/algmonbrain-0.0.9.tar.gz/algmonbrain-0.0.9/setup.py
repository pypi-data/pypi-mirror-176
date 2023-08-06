import setuptools

with open("README.md", "r",encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algmonbrain",
    version="0.0.9",
    author="algmon",
    author_email="support@algmon.com",
    description="add sth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

