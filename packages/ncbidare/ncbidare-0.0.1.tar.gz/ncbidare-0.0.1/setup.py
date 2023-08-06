from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ncbidare",
    version="0.0.1",
    author="Riddhi Sera",
    author_email="riddhisera@gmail.com",
    description="Fetch NCBI data efficiently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/riddhisera/microbio",
    install_requires = [
        "biopython~=1.78",
    ],
    extras_require = {
        "dev":[
            "pytest>=3.7",
        ],
    },
    py_modules=["ncbiget"],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)