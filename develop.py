#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Package :CNLib                                                  /          \
# Filename: develop.py                                            |     ()     |
# Date    : 01/01/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The develop script for this project.

This file sets up a virtual environment for developing the project. The main
purpose is to get the venv name right.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import locale
from pathlib import Path
import subprocess
import sys

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get prj dir path
P_DIR_PRJ = Path(__file__).parent.resolve()

# gettext stuff for CLI
S_DOMAIN = "cnlib"
P_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"
TRANSLATION = gettext.translation(S_DOMAIN, P_DIR_LOCALE, fallback=True)
_ = TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.setlocale(locale.LC_ALL, "")
locale.bindtextdomain(S_DOMAIN, P_DIR_LOCALE)

# folder and file names
S_NAME_VENV = ".venv-cnlib"
S_FILE_REQS = "requirements.txt"

# messages

# I18N: done with step
S_MSG_DONE = _("Done")
# I18N: step failed
S_MSG_FAIL = _("Failed")
# I18N: show the venv step
S_MSG_VENV_START = _("Making venv folder... ")
# I18N: show the reqs step
S_MSG_REQS_START = _("Installing requirements... ")

# errors

# I18N: an error occurred
S_ERR_ERROR = _("Error: ")

# commands

# NB: format param is dir_venv
S_CMD_CREATE = "python3 -m venv {}"
# install reqs/self
S_CMD_TYPE_INST = (
    # NB: format params are P_DIR_PRJ, S_NAME_VENV, S_FILE_REQS
    "cd {};. {}/bin/activate;python3 -m pip install -r {};"
    # NB: format params are P_DIR_PRJ, S_NAME_VENV
    "cd {};. {}/bin/activate;python3 -m pip install -e ."
)

# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Make a virtual environment for this program on the user's computer
# ------------------------------------------------------------------------------
def _make_venv():
    """
    Make a virtual environment for this program on the user's computer.
    """

    # show progress
    print(S_MSG_VENV_START, flush=True, end="")

    # the command to create a venv
    cmd = S_CMD_CREATE.format(S_NAME_VENV)
    _do_command(cmd)


# ------------------------------------------------------------------------------
# IInstall the project's requirements.txt
# ------------------------------------------------------------------------------
def _install_reqs():
    """
    Install the project's requirements.txt.
    """

    # show progress
    print(S_MSG_REQS_START, flush=True, end="")

    # the cmd to install the reqs
    # NB: for apps, the last two fmt params are ignored (no self install)
    cmd = S_CMD_TYPE_INST.format(
        P_DIR_PRJ,
        S_NAME_VENV,
        S_FILE_REQS,  # for reqs
        P_DIR_PRJ,
        S_NAME_VENV,  # for self
    )
    _do_command(cmd)


# ------------------------------------------------------------------------------
# Common code to run a shell command
# ------------------------------------------------------------------------------
def _do_command(cmd: str):
    """
    Common code to run a shell command.

    Parameters:
        cmd (str): Command to run.

    This function is just a wrapper around subprocess, to make it a little
    easier to call and return.
    """

    try:
        # NB: hide output
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(S_MSG_DONE)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(S_MSG_FAIL)
        print()
        print(S_ERR_ERROR, e)
        sys.exit(1)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line, rather than imported.

    # This file should NEVER be imported, but only run from the command line.
    # it is marked as runnable in Linux.

    # make the venv on the user's comp
    _make_venv()

    # install reqs
    _install_reqs()

# -)
