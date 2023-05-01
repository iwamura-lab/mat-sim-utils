from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ganson_utils",
    version="0.1.0",
    author="Taiki Iwamura",
    author_email="takki.0206@gmail.com",
    description="command line interface based utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwamura-lab/utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "click",
        "ase",
        "pymatgen",
    ],
    entry_points={
        "console_scripts": [
            "bump_version=ganson_utils.bump_version:cli",
            "submit_jobs=ganson_utils.scripts.submit_jobs:main",
            "show_mem_alloc=ganson_utils.scripts.show_mem_alloc:main",
            "structure_converter=ganson_utils.scripts.structure_converter:main",
        ],
    },
)
