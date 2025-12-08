<!----------------------------------------------------------------------------->
<!-- Project : CNLib                                           /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 06/12/2025                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# ![Logo](images/cnlib.png) CNLib

## "It mostly works" ™©®

[![License: WTFPLv2](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net)

<!-- __RM_SHORT_DESC__ -->
A Python library containing useful functions and classes 
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
Version 0.0.12
<!-- __RM_VERSION__ -->

<!-- __RM_SCREENSHOT__ -->
<!-- __RM_SCREENSHOT__ -->

## Table of Contents
- [Requirements](#requirements)
- [Downloading](#downloading)
- [Installing](#installing)
- [Usage](#usage)
- [Uninstalling](#uninstalling)
- [Documentation](#documentation)
- [Developing](#developing)
- [Notes](#notes)

## Requirements
<!-- __RM_DEPS__ -->
[Python 3.10+](https://python.org)
<!-- __RM_DEPS__ -->

## Downloading

There are two ways to get the code:

1. Download the [latest
release](https://github.com/cyclopticnerve/CNLib/releases/latest) (the
**'Source code (zip)'** file should work an all platforms).

2. Or you can clone the git repo to get the latest (and often broken) code from
   the main branch:
```bash
$ git clone https://github.com/cyclopticnerve/CNLib
```

## Installing
<!-- __RM_PKG__ -->
There are also two ways to get CNLib into your project.
Run these commands from your project directory.

First make sure you have a venv and it is active:
```bash
$  python -m venv .venv
$ . .venv/bin/activate
```

### Manually

If you downloaded the zip file:
```bash
$ python -m pip install /path/to//CNLib-<version>.zip
```
where \<version\> is the version number included in the file name.

Or if you cloned the repo:
```bash
$ python -m pip install /path/to/CNLib
```

### Automagically
Add this line to your project's 'requirements.txt' file:
```bash
CNLib @ git+https://github.com/cyclopticnerve/CNLib@<tag>
```
where \<tag\> is the tag you want, such as 'v0.0.1', etc.

Then run:
```
$ python -m pip install -r requirements.txt
```
<!-- __RM_PKG__ -->

## Usage
Read the [documentation](https://cyclopticnerve.github.io/CNLib/).

## Uninstalling
<!-- __RM_PKG__ -->
In your project folder:
```bash
$ . .venv/bin/activate
$ python -m pip uninstall cnlib
```
<!-- __RM_PKG__ -->

## Documentation
See the [documentation](https://cyclopticnerve.github.io/CNLib).

## Developing
If you are developing this project, make sure you run the "develop.py" script
first to create the proper virtual environment (venv). 

## Notes
10/10, no notes.

-)
<!-- -) -->
