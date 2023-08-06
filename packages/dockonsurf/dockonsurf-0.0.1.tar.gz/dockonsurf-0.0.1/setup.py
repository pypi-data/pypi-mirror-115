# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as readme_fh:
    long_description = readme_fh.read()

setup(
    name="dockonsurf",  # Replace with your own username
    version="0.0.1",
    author="Carles Martí",
    author_email="carles.marti2@gmail.com",
    description="Code to systematically find the most stable geometry for "
                "molecules on surfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://forge.cbp.ens-lyon.fr/redmine/projects/dockonsurf",
    project_urls={
        "Documentation": "https://dockonsurf.readthedocs.io",
    },
    # package_dir={"": "dockonsurf"},
    packages=find_packages(where='dockonsurf'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Chemistry",

    ],
    python_requires='>=3.6',
    install_requires=[
        "ase>=3.19.1",
        "hdbscan~=0.8.26",
        "matplotlib>=3.2.1",
        "networkx>=2.4",
        "numpy>=1.16.6",
        "pycp2k~=0.2.2",
        "pymatgen~=2020.11.11",
        "python-daemon~=2.2.4",
        "rdkit>=2019.9.3",
        "scikit-learn~=0.23.1",
    ],

)
