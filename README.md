<!----------------------------------------------------------------------------->
<!-- Project : CNLib                                           /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 06/12/2025                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

![](images/cnlib.png)
# CNLib

## "It mostly works" ™©®

[![License: WTFPLv2](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net)

<!-- __RM_SHORT_DESC__ -->
A library to support PyPlate and PyPlate projects
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
Version 0.0.1
<!-- __RM_VERSION__ -->

<!-- ![alt-text](readme/screenshot.png) -->

## Table of Contents
- [Requirements](#requirements)
- [Downloading](#downloading)
- [Installing](#installing)
- [Uninstalling](#uninstalling)
- [Usage](#usage)
- [Notes](#notes)

## Requirements
<!-- __RM_DEPS__ -->
[Python 3.10+](https://python.org)
<!-- __RM_DEPS__ -->

## Downloading

There are two ways to get the package:

1. Download the [latest
release](https://github.com/cyclopticnerve/CNLib/releases/latest) (the
**'Source code (zip)'**
file should work an all platforms).


2. Or you can clone the git repo to get the latest (and often broken) code from
   the main branch:
```bash
$ git clone https://github.com/cyclopticnerve/CNLib
```

## Installing
<!-- __RM_PKG__ -->
There are also two ways to get CNLib into your project:

### Manually

First make sure you have a venv and it is active:
```bash
$  python -m venv .venv
$ . .venv/bin/activate
```

Then, if you downloaded the zip:
```bash
$ python -m pip install /path/to//CNLib-<version>.zip
```

If you cloned the repo or unzipped the file:
```bash
$ python -m pip install /path/to/CNLib
```

### Automagically
Add this line to your 'requirements.txt" file:
```bash
CNLib @ git+https://github.com/cyclopticnerve/CNLib@releases/latest
```
Then run:
```
$ python -m pi install -r requirements.txt
```

<!-- __RM_PKG__ -->

## Usage
HTML documentation can be found in the CNLib-\<version\>/docs folder.

## Uninstalling
<!-- __RM_PKG__ -->
In your project folder:
```bash
$ . .venv/bin/activate
$ python -m pip uninstall cnlib
```
<!-- __RM_PKG__ -->

## Notes
10/10, no notes.

-)
<!-- -) -->
