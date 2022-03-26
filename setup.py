from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="utils",
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
    py_modules=["bump_version"],
    python_requires=">=3.7",
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        bump_version=bump_version:cli
    """,
)
