"""
Create Whl: python setup.py sdist bdist_wheel
Local installation: python -m pip install dist/[name-of-whl]
Push to pip: python -m twine upload dist/*
"""

from pathlib import Path

from setuptools import setup, find_packages


readme = Path("README.md")
long_description = readme.read_text()

setup(
    name='non-linear-shrinkage',
    version='1.0.0',
    description="Non-Linear Shrinkage Estimator from Ledoit and Wolf (2018) ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shoemakerdr/analytic_shrinkage",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    python_requires=">=3.6",
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
