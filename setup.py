from pathlib import Path

import setuptools

VERSION = "1.3.1"  # PEP-440

NAME = "pelican-fediverse"

INSTALL_REQUIRES = [
    "streamlit>=1.32.0",
    "gspread>=5.8.0, <6",
    "gspread-pandas>=3.2.2",
    "gspread-dataframe>=3.3.0",
    "gspread-formatting>=1.1.2",
    "duckdb>=0.8.1",
    "sql-metadata>=2.7.0",
    "validators>=0.22.0",
]


setuptools.setup(
    name=pelican-fediverse,
    version=1.3.1,
    description="A Pelican plugin to publish content on the Fediverse",
    url="https://github.com/pelican-plugins/fediverse",
    project_urls={
        "Source Code": "https://github.com/pelican-plugins/fediverse",
    },
    author="Maurizio Paglia",
    author_email="maurizio@mauriziopaglia.it",
    license="GPL License 3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GPL Software License",
        "Programming Language :: Python :: 3.10",
    ],
    # Snowpark requires Python 3.8
    python_requires=">=3.9",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["streamlit_gsheets"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)