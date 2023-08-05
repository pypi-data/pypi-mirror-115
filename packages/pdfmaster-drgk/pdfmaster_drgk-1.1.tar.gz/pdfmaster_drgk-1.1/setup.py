import setuptools
from pathlib import Path

setuptools.setup(
    name="pdfmaster_drgk",  # unique name so doesnt clash with other on PyPi.org
    version=1.1,
    long_description=Path("README.md").read_text(),
    # set it to content of readme file
    packages=setuptools.find_packages(
        exclude=["tests", "data/"])  # excluded these 2 folders
)
