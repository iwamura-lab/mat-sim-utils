# mat-sim-utils

CLI applications for materials simulation

## Overview

This repository holds various CLI applications for materials simulation. By installing this package, you can utilize various commands convenient when simulating materials.

## Installation

Git clone this repository and run following commands.

```shell
$ cd <mat-sim-utils root>
$ pip install .
```

## Usage

After installation, you can use 4 commands explained below. You can display helpfull messages by executing commands with `--help` option. For example,

```shell
$ bump_version --help
Usage: bump_version [OPTIONS] NEW_VERSION_NUM

  This script changes package's version number.

Options:
  --help  Show this message and exit.
```

### bump_version

This command is for another Python package. This changes the version numbers written in `setup.py` and `setup.cfg`.

### submit_jobs

This command submits VASP jobs to Sun Grid Engine.

### show_mem_alloc

This command shows current memory allocation of your jobs.

### structure_converter

This command converts a lammps-data format structure file to a POSCAR format structure file, and vice versa.
