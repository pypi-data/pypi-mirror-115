from setuptools import setup

from SplitStrains import __version__, _program


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=_program,
    version=__version__,
    author="Einar Gabbasov",
    author_email="",
    description="SplitStrains detects and separates mixed strains of Mycobacterium tuberculosis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WGS-TB/SplitStrains",
    license="",
    packages=["SplitStrains"],
    entry_points="""
    [console_scripts]
    {program} = SplitStrains.splitStrains:main
    """.format(program=_program),
    include_package_data=True,
    install_requires=[
        "matplotlib>=3.3",
        "mixem",
        "numpy>=1.15",
        "pysam",
        "scikit-learn",
        "scipy>=1.0",
        "seaborn",
    ],
)
