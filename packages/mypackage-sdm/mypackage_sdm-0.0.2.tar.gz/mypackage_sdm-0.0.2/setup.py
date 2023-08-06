from setuptools import setup
from runpy import run_path

__version__ = run_path("src/my_prj_name/version.py")["__version__"]

setup(
    name='mypackage_sdm',
    author="Samuel Demir",
    author_email="demir.samuel@outlook.de",
    description="This project is for testing purposes",
    version=__version__,
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    license="MIT",
    platforms="any",
    python_requires=">=3.8",
)
