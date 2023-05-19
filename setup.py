from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

structure_converter_src = "mat_sim_utils.scripts.structure_converter:main"

setup(
    name="mat_sim_utils",
    version="1.1.0",
    author="Taiki Iwamura",
    author_email="takki.0206@gmail.com",
    description="command line interface based utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwamura-lab/mat-sim-utils",
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
        "pymatgen>=2023.5.10",
    ],
    entry_points={
        "console_scripts": [
            "bump_version=mat_sim_utils.bump_version:cli",
            "submit_jobs=mat_sim_utils.scripts.submit_jobs:main",
            "show_mem_alloc=mat_sim_utils.scripts.show_mem_alloc:main",
            f"structure_converter={structure_converter_src}",
        ],
    },
)
