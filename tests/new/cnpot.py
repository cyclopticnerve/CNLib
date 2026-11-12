""" docstring """

# 2. extract (produce a .pot file)

# DEBUG: these imports are for debug only
from pathlib import Path
from shutil import rmtree

# imports
from subprocess import run, SubprocessError

# DEBUG: make file struct thus far
dir_i18n = Path("tests/new/i18n")
# NB: trust me...
if dir_i18n.exists():
    rmtree(dir_i18n)  # nuke old
dir_i18n.mkdir()  # make new

# extract command
cmd = [
    "xgettext",
    # ------------------------------
    # output options
    # path/name of pot file to produce (path rel to cwd)
    "--output=tests/new/i18n/domain.pot",
    # ------------------------------
    # clang options
    # --language={}
    # ------------------------------
    # operation mode
    # -----
    # comments
    # "-c",       # all comments
    "-cI18N:",  # backtrack to first occurrence of "I18N:"
    # -----
    # TODO: when to use?
    "--keyword=_p:1,2",
    # ------------------------------
    # output details
    "--sort-by-file",
    # copyright (first comment block in pot/po)
    # ALL PUBLIC DOMAIN!!!
    # absent: parent prj
    # "--copyright-holder=",  # pub dom
    # or
    "--foreign-user",
    # "--copyright-holder=boogers@gmail.com",
    "--package-name=MyProject",
    "--package-version=0.0.2",
    "--msgid-bugs-address=https://github.com/cyclopticnerve",
    # ------------------------------
    # input files
    # ------------------------------
    "tests/new/src/python/source.py",
    # "tests/steps/template.desktop",
    # "tests/steps/gui.ui",
    # "tests/steps/gui.glade",
]

# run cmd
try:
    cp = run(cmd, check=True)
except SubprocessError as e:
    print(e)

# TODO: still need to fix:
#
# comments:
# SOME DESCRIPTIVE TITLE.
# replace  with'Translation template for MyProject package.'
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
# header:
# CHARSET

# handle .ui files
# make po/LINGUAS file

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# init

# update

#translate

# compile

# desktop
