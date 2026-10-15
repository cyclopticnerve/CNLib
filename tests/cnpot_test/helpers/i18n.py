# ------------------------------------------------------------------------------
# Package : __PP_NAME_BIG__                                        /          \
# Filename:                                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A helper module for i18n.

This module creates a singleton CNPotPy object for use in a Python project. The
object is created the first time this file is imported/run.

To get "i18n strings" in a source file, simply import the underscore function:

    from tests.cnpot_test.helpers.i18n import _

Then in your code, define strings like this:

    a_str = _("A string in English")

See CNLib/tests/cnpot_test/src/python/source.py for an example.

You can create or update all your i18n files from any module that imports
this module, like this:

    from tests.cnpot_test.helpers.i18n import potpy

    potpy.main()

See CNLib/tests/cnpot_test/helpers/run.py for an example.

You can also use this file as a task in your IDE, or run it from a terminal.
Make sure that _P_DIR_PRJ (below) points to your project's top directory. Also
make sure that your project's venv is active. (This trips me up ALL THE TIME!)

If you are developing a GUI program, you can also use strings displayed in
UI controls. See CNLib/tests/cnpot_test/src/gui.glade (or gui.ui in the same
folder, both if these should work) for an example.

If you want to know why the imports look the way they do (AND WORK!!!), see:
    https://stackoverflow.com/a/50193944

    TLDR:
    1. Use a "pyproject.toml" file in your project. You can find an
        example implementation of "pyproject.toml" in "CNLib/misc".

        Make sure to remove the ".example" suffix before using (this is to
        prevent the file being recognized twice in CNLib).

    2. Install your project as editable in its own venv, like this:

        $ cd MyProject
        $ pip install -e .

    3. PROFIT!!!

If you want to know more about CNPotPy, see CNLib/cnlib/cnpot.py.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# cnlib imports
from cnlib import cnfunctions as F
from cnlib import cnpot

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# path to project dir (this file's parent/parent folder)
_P_DIR_PRJ = Path(__file__).parents[1].resolve()  # "/path/to/cnpot_test"

# ------------------------------------------------------------------------------
# Objects
# ------------------------------------------------------------------------------

potpy = None

# create singleton CNPotPy
try:
    potpy = cnpot.CNPotPy(
        # start searching from here
        # path must be absolute
        project_path=_P_DIR_PRJ,
        # path to i18n dir (absolute, or relative to project_dir)
        # default: project_dir / "i18n"
        i18n_path=_P_DIR_PRJ / "i18n",
        # list of paths to search (absolute, relative, glob; files or dirs)
        # default: [project_dir]
        source_paths=[_P_DIR_PRJ],
        # domain name (name of .mo files in locale subdirs, same as underscore)
        # default: project_dir.name
        domain=_P_DIR_PRJ.name,
        # version
        # default: None
        version="0.0.1",
        # author
        # default: None
        author="cyclopticnerve",
        # author's email (NOT translator)
        # default: None
        email="cyclopticnerve@gmail.com",
        # the tag to stop regressive context/comment search
        # default: None
        tag="I18N",
        # file encoding
        # default: "UTF-8"
        # encoding="UTF-8",
        # dict of computer language names and their extensions
        # default: {
        #     "Python": [".py"],
        #     "Glade": [".ui", ".glade"],
        #     "Desktop": [".desktop"],
        # }
        # see "man xgettext" for a full list of clang names
        clangs_dict={
            "Python": [".py"],
            "Glade": [".ui", ".glade"],
            "Desktop": [".desktop"],
        },
        # path to template .desktop file
        # default: None
        desk_in_path=_P_DIR_PRJ / "src/template.desktop",
        # path to i18n'ed desktop file
        # default: None
        desk_out_path=_P_DIR_PRJ / "i18n/desktop/cnpot_test.desktop",
    )

# init throws error if prj path is none/"", not abs, or not exist
except ValueError as e:
    print(e)

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

# get alias to underscore function
_ = str
if potpy:
    _ = potpy.underscore()

# test for empty translation
string = _("")
"""string = _(" ")"""

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    print("running i18n.py from terminal")

    # do the thing
    if potpy:
        try:
        # "That's all, folks!" -- Mel Blanc
            potpy.main()

        # main raises OSError if xgt not found
        except OSError as e:
            print(e)

        # main raises CNRunError if any step fails
        except F.CNRunError as e:
            print(e)

# -)
