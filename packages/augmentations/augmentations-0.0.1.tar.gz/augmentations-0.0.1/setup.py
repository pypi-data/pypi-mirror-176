"""Setup."""

from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "wheel",
    "Cython>=0.29.0",
    "numpy>=1.23.0",
    "scikit-image>=0.19.0",
    "pillow>=9.0.1",
    "geojson>=2.5.0",
    "scipy>=1.9.1",
    "Shapely>=1.8.4",
    "turfpy>=0.0.7",
    "rasterio>=1.3.0",
]

setup(
    name="augmentations",
    version="0.0.1",
    description="Roboflow Augmentations PIP Package",
    long_description_content_type="text/markdown",
    author="Roboflow",
    author_email="jim@roboflow.com",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=["Programming Language :: Python :: 3.10"],
)
