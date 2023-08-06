import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fhawp",
    version="0.0.6",
    author="will judd",
    author_email="wsjudd@gmail.com",
    description="four hours a week project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silentdragoon/fhawp",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)