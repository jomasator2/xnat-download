# pip3 install setuptools twine wheel
# python3 setup.py sdist bdist_wheel
# twine upload dist/*


import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with (HERE / "requirements.txt").open() as f:
    requirements = f.read().splitlines()

setup(
    name="xnat_downloader",
    version="0.1.20231123",
    description="Download XNAT project with python requests",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BIMCV-CSUSP/xnat-download",
    author="Jose Manuel Saborit-Torres & Alejandro Mora-Rubio",
    author_email="josemanuel.saborit@fisabio.es",
    license="GNU GPLv3",
    entry_points={
        "console_scripts": [
            "xnat_downloader = xnat_downloader.__main__:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research"
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
