from setuptools import find_packages, setup

# Read in the version number
exec(open("src/hierarchy/version.py", "r").read())

setup(
    name="hierarchy",
    version=__version__,
    # install_requires=requirements,
    author="Vince Knight and Nikoleta E. Glynatsi",
    author_email=("knightva@cardiff.ac.uk"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="",
    license="The MIT License (MIT)",
)
