# ------------------------------------------------------------------------------
# Package : CNLib                                                  /          \
# Filename: cnpot.py                                              |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines

"""
Run GNU gettext tools to create i18n files for a project.

This class converts all marked strings in source files to i18n versions using
xgettext, and creates .po files in the i18n/po directory. It also uses msgfmt
and msgmerge to convert .po files to .mo files in the i18n/mo directory.

The class can handle all xgettext's supported file types by using each language
name as the key for a list of file extensions in a dictionary.

Note that the word "language" here can refer either to the computer language of
the input file (ie. "Python", "Glade") or the written language of the output
file (ie. "English", "Spanish"). I have tried to disambiguate this by using
"clang(s)" to refer to the former, and "wlang(s)" to refer to the latter.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from datetime import date
import gettext
import locale
from pathlib import Path
import re
import shutil
from typing import Callable

# cnlib imports
import cnlib.cnfunctions as F

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to handle making the I18N files for a Python project
# ------------------------------------------------------------------------------
class CNPotPy:
    """
    A class to handle making the I18N files for a Python project.

    This class provides methods to create .pot, .po, .mo, and .desktop files
    for internationalizing a CLI or GUI project.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Strings
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # commands

    # check if xgettext is installed
    _S_CMD_WHICH_XGT = "which xgettext"
    # call xgettext
    # NB: format params are... see below
    _S_CMD_XGT = (
        # call GNU tool
        "xgettext "
        # output file
        # NB: param is self._path_pot (as quoted string)
        "--output={} "
        # language of file to be scanned
        # NB: param is clang_name
        "--language={} "
        # join with existing .pot file
        "--join-existing "
        # comment handling (see docs)
        # NB: param is self._str_tag
        "--add-comments={} "
        # sort entries by file
        "--sort-by-file "
        # fix license string
        # NB: param is self._str_domain
        "--package-name={} "
        # set version number
        # NB: param is self._str_version
        "--package-version={} "
        # set email address for bugs
        # NB: param is self._str_email
        "--msgid-bugs-address={} "
        # path(s) to src files
        # NB: param is str_clang_files
        "{}"
    )
    # shell commands to make po/mo
    # NB: format params are file_po and self._path_pot
    # NB: no backup! DANGER WILL ROBINSON! -- fuck im old
    _S_CMD_MERGE_POS = "msgmerge --update --backup=none {} {}"
    # NB: format params are file_mo and file_po
    _S_CMD_MAKE_MOS = "msgfmt --output-file={} {}"
    # NB: format params are path_desk_in, path_desk_out, path_po
    _S_CMD_DESK = "msgfmt --desktop --template={} --output-file={} -d {}"

    # --------------------------------------------------------------------------
    # dirs

    # fixed GNU dir under locale dir
    _S_DIR_LC = "LC_MESSAGES"

    # --------------------------------------------------------------------------
    # files

    # fixed GNU file to store all wlang names for .desktop files
    _S_FILE_LINGUAS = "LINGUAS"

    # --------------------------------------------------------------------------
    # exts

    # fixed GNU file extensions
    _S_EXT_POT = ".pot"
    _S_EXT_PO = ".po"
    _S_EXT_MO = ".mo"

    # --------------------------------------------------------------------------
    # errors

    # error message for project path is not absolute
    # NB: format param is project_path
    _S_ERR_PRJ_NO_PATH = "ERROR: project_path does not exist: {}"
    # error message for no xgettext
    _S_ERR_NO_XGT = "ERROR: No xgettext, use 'sudo apt install gettext'"

    # --------------------------------------------------------------------------
    # warnings

    # warning message for source does not exist
    # NB: format param is source path
    _S_WARN_NO_SRC = "WARNING: source_path does not exist: {}"
    # warning message for no lang in po file
    # NB: format param is file name
    _S_WARN_NO_LANG = "WARNING: No language set in po file: {}"
    # warning for empty string
    # NB: format params are file path and line number
    _S_WARN_EMPTY_TRANS = "WARNING: Empty translation value: {}:{}"

    # --------------------------------------------------------------------------
    # default params of my personal choosing (deal with it)

    # default base folder for all i18n stuff (under prj)
    # NB: this is the only name that is not a param, since it can be specified
    # in __init__'s i18n_path
    _S_DEF_DIR_I18N = "i18n"
    # default name of locale dir (under i18n_path)
    _S_DEF_DIR_LOCALE = "locale"
    # default dir name for po files (under i18n_path)
    _S_DEF_DIR_PO = "po"
    # default encoding for .pot and .po files
    _S_DEF_ENCODING = "UTF-8"

    # --------------------------------------------------------------------------
    # Regex strings
    # --------------------------------------------------------------------------

    # title
    _R_TITLE_SCH = r"# SOME DESCRIPTIVE TITLE."
    # NB: format param is self._str_domain
    _R_TITLE_REP = r"# {} translation template"
    # copyright
    _R_COPY_SCH = (
        r"(# Copyright \(C\) )(YEAR)( )(THE PACKAGE'S COPYRIGHT HOLDER)"
    )
    # NB: format params are current year and author param
    _R_COPY_REP = r"\g<1>{}\g<3>{}"
    # author email
    _R_AUTH_SCH = r"(# FIRST AUTHOR )(<EMAIL@ADDRESS>)(, )(YEAR)"
    # NB: format params are email param and current year
    _R_AUTH_REP = r"\g<1>{}\g<3>{}"
    # wlang inside file
    _R_LANG_SCH = r"(\"Language: )(.*?)(\\n\")"
    # empty translation string (borks .pot output)
    _R_EMPTY_SCH = r"^[^#]*_\([\"|'] *[\"|']\)"

    # --------------------------------------------------------------------------
    # Lists
    # --------------------------------------------------------------------------

    # list of extensions to search for empty translations (i.e. '_("")')
    # NB: this makes searching a little more efficient
    _L_EMPTY_TRANS = ["Python"]

    # --------------------------------------------------------------------------
    # Dictionaries
    # --------------------------------------------------------------------------

    # default clang dict
    _D_CLANGS = {
        "Python": [".py"],
        "Glade": [".ui", ".glade"],
        "Desktop": [".desktop"],
    }

    # --------------------------------------------------------------------------
    # Objects
    # --------------------------------------------------------------------------

    # singleton instance
    _O_INST = None

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Create a new object from a class
    # --------------------------------------------------------------------------
    # NB: type hinting here is IMPOSSIBRUUUU!!!
    def __new__(cls, *args, **kwargs):
        """
        Create a new object from a class.

        This is the usual implementation of a singleton class in Python. Note
        that *args and **kwargs are unused, but necessary. Python is weird lol.

        Args:
            cls: The class type of the object to create.
            *args: A list of all the positional arguments to the class' creator
                function.
            **kwargs: A dictionary of all the keyword arguments to the class'
                creator function.

        Returns:
            A new or existing object of the specified class.
        """

        # if no previous instance
        if not cls._O_INST:

            # create an instance
            cls._O_INST = super().__new__(cls)

        # return whatever we found/created
        return cls._O_INST

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        # ----------------------------------------------------------------------
        # input
        # start dir (for relative paths)
        project_path: Path,
        # list of input folders/files (abs/rel Path)
        source_paths: list[Path] | None = None,
        # set clangs (override default, NOT combine)
        clangs_dict: dict[str, list[str]] | None = None,
        # ----------------------------------------------------------------------
        # output
        # output dir
        i18n_path: Path | None = None,
        # locale dir under output dir
        locale_name: str | None = None,
        # po dir under output dir
        po_name: str | None = None,
        # .pot/.mo file name
        domain: str | None = None,
        # ----------------------------------------------------------------------
        # meta
        # project version
        version: str | None = None,
        # project author
        author: str | None = None,
        # project author email
        email: str | None = None,
        # tag to stop regressive context search
        tag: str | None = None,
        # ----------------------------------------------------------------------
        # desktop stuff
        # path to template desktop
        desk_in_path: Path | None = None,
        # path to final desktop
        desk_out_path: Path | None = None,
    ):
        """
        Initialize the new object.

        Initializes a new instance of the class, setting the specified or
        default values of its properties, and any other code needed to create a
        new object.

        Args:
            project_path: The main project Path, used for relative paths. This
                Path is required. If the Path is relative, is it resolved
                against the current working directory.
            source_paths: The list of Paths to folders and files to be scanned.
                Consider this a 'whitelist'. Paths can be absolute or relative
                to project_path. Paths can also be folders or files.
                (default: None, use project_path)
            clangs_dict: The dictionary of file extensions to scan for each
                clang. For each entry, the key is a clang known to xgettext.
                The value is a list of file extensions associated with that
                clang. (default: None, use self._D_CLANGS)
            i18n_path: The directory to place all i18n folders/files. Path can
                be absolute or relative to project_path. (default: None, use
                project_path / "i18n")
            locale_name: The name of the locale folder under i18n_path.
                (default: None, use "locale")
            po_name: The name of the po folder under i18n_path. (default: None,
                use "po")
            domain: The name of the domain (program name). This name should
                be unique to you program. (default: None, use
                project_path.name)
            version: Version info to use in .pot/.po header. (default: None,
                do not replace)
            author: Author name to use in .pot/.po header. (default: None, do
                not replace)
            email: Email to use in .pot/.po header. (default: None, do not
                replace)
            tag: String that signifies a context comment. If the value is None,
                no comments are included. If the value is an empty string (""),
                all comments above the string are included as context, until a
                blank or non-comment line is found. Any other value will
                include all preceding comment lines that include "tag", until a
                blank or non-comment line is found. (default: None, no
                comments)
            desk_in_path: The path to the desktop template file. Path can be
                absolute or relative to project_path. Ignored if desk_out_path
                is None. (default: None, do not use)
            desk_out_path: The path to the desktop output file. Path can be
                absolute or relative to project_path. Ignored if desk_in_path
                is None. (default: None, do not use)

        Raises:
            ValueError: If project_path does not exist.
        """

        # ----------------------------------------------------------------------
        # sanitize all params

        # ----------------------------------------------------------------------
        # input

        # ----------------------------------------------------------------------
        # check project_path

        # if path is relative, make it abs rel to cwd
        project_path = project_path.resolve()

        # check if path is abs and exists
        if not project_path.exists():
            raise ValueError(self._S_ERR_PRJ_NO_PATH.format(project_path))

        # project_path is ok, keep going
        self._path_project = project_path

        # ----------------------------------------------------------------------
        # check source_paths

        # get default source paths (none or empty list)
        if not source_paths:
            source_paths = [self._path_project]

        # make source_paths absolute
        source_paths = [
            item if item.is_absolute() else self._path_project / item
            for item in source_paths
        ]

        # check if all sources exist
        tmp_src_paths = []
        for source_path in source_paths:

            # does exist, add
            if source_path.exists():
                tmp_src_paths.append(source_path)

            # no exist, warn, but do not fail
            else:
                F.printc(
                    self._S_WARN_NO_SRC.format(source_path),
                    fg=F.C_FG_YELLOW,
                    bold=True,
                )

        # TODO: need to ignore venv
        # store source_paths
        self._list_sources = tmp_src_paths

        # ----------------------------------------------------------------------
        # check clangs

        # get default clangs (none or empty dict)
        if not clangs_dict:
            clangs_dict = self._D_CLANGS

        # add leading dot if necessary
        for clang, exts in clangs_dict.items():

            # check for leading dot
            exts = [
                f".{ext}" if not ext.startswith(".") else ext for ext in exts
            ]
            clangs_dict[clang] = exts

        # clangs is fixed, use it
        self._dict_clangs = clangs_dict

        # ----------------------------------------------------------------------
        # output

        # ----------------------------------------------------------------------
        # check i18n_path (none or rel)
        if not i18n_path:
            i18n_path = self._path_project / self._S_DEF_DIR_I18N
        if not i18n_path.is_absolute():
            i18n_path = self._path_project / i18n_path
        self._path_i18n = i18n_path

        # ----------------------------------------------------------------------
        # make locale path (none or empty)
        if not locale_name:
            locale_name = self._S_DEF_DIR_LOCALE
        self._path_locale = self._path_i18n / locale_name

        # ----------------------------------------------------------------------
        # make po path (none or empty)
        if not po_name:
            po_name = self._S_DEF_DIR_PO
        self._path_po = self._path_i18n / po_name

        # ----------------------------------------------------------------------
        # get domain (none or empty)
        if not domain:
            domain = self._path_project.name
        self._str_domain = domain

        # ----------------------------------------------------------------------
        # meta

        # just store args as props (none/empty/whatever)
        self._str_version = version
        self._str_author = author
        self._str_email = email

        # TODO: test this
        # None: use no comments
        # "": use all comments

        # get tag
        if tag is None:
            tag = ""
        elif tag == "":
            tag = None
        self._str_tag = tag

        # ----------------------------------------------------------------------
        # desktop stuff

        # we have something in, make it absolute
        if desk_in_path and not desk_in_path.is_absolute():
            desk_in_path = self._path_project / desk_in_path
        # store abs path or None
        self._path_desk_in = desk_in_path

        # we have something out, make it absolute
        if desk_out_path and not desk_out_path.is_absolute():
            desk_out_path = self._path_project / desk_out_path
        # store abs path or None
        self._path_desk_out = desk_out_path

        # ----------------------------------------------------------------------

        # make refs to folder structure (but DO NOT create)
        self._path_pot = self._path_i18n / f"{self._str_domain}{self._S_EXT_POT}"
        self._file_mo = f"{self._str_domain}{self._S_EXT_MO}"
        self._path_linguas = self._path_po / self._S_FILE_LINGUAS

        # store files to search
        self._dict_src_files = {}

        # default list of po files
        self._list_pos = []

        # ----------------------------------------------------------------------

        print()

        print("----- input -----")
        print("self._path_project:", self._path_project)
        F.pp(self._list_sources, label="self._list_sources")
        F.pp(self._dict_clangs, label="self._dict_clangs")

        print("----- output -----")
        print("self._path_i18n:", self._path_i18n)
        print("self._path_locale:", self._path_locale)
        print("self._path_po:", self._path_po)
        print("self._str_domain:", self._str_domain)

        print("----- meta -----")
        print("self._str_version:", self._str_version)
        print("self._str_author:", self._str_author)
        print("self._str_email:", self._str_email)
        print("self._str_tag:", self._str_tag)

        print("----- desktop -----")
        print("self._path_desk_in:", self._path_desk_in)
        print("self._path_desk_out:", self._path_desk_out)

        print("----- paths -----")
        print("self._path_pot:", self._path_pot)
        print("self._file_mo:", self._file_mo)
        print("self._path_linguas:", self._path_linguas)

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Return the underscore function
    # --------------------------------------------------------------------------
    def underscore(self) -> Callable[[str], str]:
        """
        Return the underscore function.

        This is the function that source files import and use to mark strings
        as translatable. See tests/cnpot_test/src/python/source.py for an
        example.

        Returns:
            The gettext method to be used in Python source files.
        """

        # TODO: maybe make this a module level func so no obj needed

        # fix locale (mostly for GUI?)
        locale.setlocale(locale.LC_ALL, "")
        locale.bindtextdomain(self._str_domain, self._path_locale)

        # get a translation object
        translation = gettext.translation(
            self._str_domain, self._path_locale, fallback=True
        )

        # return translation object's gettext method
        return translation.gettext

    # --------------------------------------------------------------------------
    # Run the main method to make or update the files
    # --------------------------------------------------------------------------
    def main(self):
        """
        Run the main method to make or update the files.

        The main method of the class, performing its steps. This method can
        (and should) be run, in Mayor Tweed's words, "early and often". You
        should run it every time a source file that contains i18n strings is
        added, edited, or deleted. You should also run it after a language .po
        file is added, edited, or deleted.

        Raises:
            OSError: If xgettext cannot be found.
            cnlib.cnfunctions.CNRunError: If any of the main steps fails.
        """

        # sanity check for xgettext
        # NB: keep this here because we can still create an object to use it's
        # underscore method, even if we have no xgt (xgt only used to make)
        try:
            F.run(self._S_CMD_WHICH_XGT, capture_output=True)
        except F.CNRunError as e:
            raise OSError(self._S_ERR_NO_XGT) from e

        # fix up source_paths every time main is run
        self._dict_src_files = self._get_source_files()

        # fix up po list every time main is run
        self._list_pos = self._get_po_files()

        # debug
        print("----- other -----")
        F.pp(self._dict_src_files, label="self._dict_src_files")
        F.pp(self._list_pos, label="self._list_pos")

        # make file structure on first run
        self._make_file_struct()

        # ----------------------------------------------------------------------
        # do the steps

        try:

            # make new .pot file
            self._make_pot()

            # make po files for new langs, or new .po files for existing langs
            self._make_pos()

            # # make .mo files for all existing .po files
            self._make_mos()

            # make desktop if template present
            self._make_desktop()

        # send errors up to caller
        except F.CNRunError as e:
            raise e

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Create a .pot file in the i18n folder
    # --------------------------------------------------------------------------
    def _make_pot(self):
        """
        Create a .pot file in the i18n folder.

        Parses the files for each clang, creating a unified .pot file, which is
        created as "i18n/<domain>.pot".

        Raises:
            cnlib.cnfunctions.CNRunError: If the make fails.
        """

        # for each clang name / list of clang files
        for clang_name, clang_files in self._dict_src_files.items():

            # sanity check (None or empty)
            if not clang_files:
                continue

            # check for empty translations strings
            # NB: makes empty search more efficient
            if clang_name in self._L_EMPTY_TRANS:
                self._check_empty_trans(clang_files)

            # convert list of paths to quoted string
            list_clang_files = [f'"{str(item)}"' for item in clang_files]
            str_clang_files = " ".join(list_clang_files)

            # get the cmd
            cmd = self._S_CMD_XGT.format(
                # make path into quoted string
                f'"{str(self._path_pot)}"',  # output
                clang_name,  # language
                self._str_tag,  # --add-comments
                self._str_domain,  # --package-name
                self._str_version,  # --package-version
                self._str_email,  # --msgid-bugs-address
                str_clang_files,  # list of quoted files to scan
            )

            # do the final command
            try:
                F.run(cmd, capture_output=True)
            except F.CNRunError as e:
                raise e

            # fix copyright/email/version in pot
            self._fix_pot_header()

    # --------------------------------------------------------------------------
    # Merge any .po files in the po folder with new/existing .pot file
    # --------------------------------------------------------------------------
    def _make_pos(self):
        """
        Merge any .po files in the po folder with new/existing .pot file.

        Whenever a new .pot file is generated using _make_pot, this method will
        produce a new .po file for each wlang that contains the difference
        between the new .pot file and the existing .po file.

        This new .po file should be sent to the translator for each wlang. Then
        when the translator sends back the translated .po file, place it in the
        po directory. Then run main() to create a new .mo file.

        Raises:
            cnlib.cnfunctions.CNRunError: If the make fails.
        """

        # sanity check (None or empty)
        if not self._list_pos:
            return

        # quote erthin
        q_path_pot = f'"{str(self._path_pot)}"'

        # for each wlang in the po folder
        for file_po in self._list_pos:

            # quote erthin
            q_file_po = f'"{str(file_po)}"'

            # update existing po file using latest pot
            cmd = self._S_CMD_MERGE_POS.format(q_file_po, q_path_pot)
            try:
                F.run(cmd, capture_output=True)
            except F.CNRunError as e:
                raise e

    # --------------------------------------------------------------------------
    # Create .mo files for all .po files and put them in the locale folder
    # --------------------------------------------------------------------------
    def _make_mos(self):
        """
        Create .mo files for all .po files and put them in the locale folder.

        Seriously, that's it. Just keep .mo files updated with .po files.

        Raises:
            cnlib.cnfunctions.CNRunError: If the make fails.
        """

        # nuke whole locale dir and recreate
        shutil.rmtree(self._path_locale)
        self._path_locale.mkdir(parents=True, exist_ok=True)

        # sanity check
        if not self._list_pos:
            return

        # for each wlang
        for file_po in self._list_pos:

            # get .mo dir (output)
            dir_mo = self._path_locale / file_po.stem / self._S_DIR_LC
            dir_mo.mkdir(parents=True, exist_ok=True)
            file_mo = dir_mo / self._file_mo

            # quote erthin
            q_file_mo = f'"{str(file_mo)}"'
            q_file_po = f'"{str(file_po)}"'

            # do the command
            cmd = self._S_CMD_MAKE_MOS.format(q_file_mo, q_file_po)
            try:
                F.run(cmd, capture_output=True)
            except F.CNRunError as e:
                raise e

    # --------------------------------------------------------------------------
    # Localize the desktop file
    # --------------------------------------------------------------------------
    def _make_desktop(self):
        """
        Localize the desktop file.

        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final desktop file. AFAIK the
        only entries that are i18n'ed are Name (which you should mark with a
        comment that says "DO NOT TRANSLATE", since you almost never want to
        i18n it) and Comment, which is a short description of your program,
        usually used in start menu tooltips and the like.

        Raises:
            cnlib.cnfunctions.CNRunError: If the make fails.
        """

        # sanity checks

        # fail silently if no input/output
        if not self._path_desk_in or not self._path_desk_out:
            return

        # ----------------------------------------------------------------------

        # write the LINGUAS file
        list_po_lang = [item.stem for item in self._list_pos]

        # make all entries into one long space separated string
        str_linguas = " ".join(list_po_lang)

        # write to linguas file
        with open(self._path_linguas, "w", encoding=self._S_DEF_ENCODING) as f:
            f.write(str_linguas)

        # ----------------------------------------------------------------------

        # quote erthin
        q_path_desk_in = f'"{self._path_desk_in}"'
        q_path_desk_out = f'"{self._path_desk_out}"'
        q_path_po = f'"{self._path_po}"'

        # do the thing
        cmd = self._S_CMD_DESK.format(
            q_path_desk_in, q_path_desk_out, q_path_po
        )
        try:
            F.run(cmd, capture_output=True)
        except F.CNRunError as e:
            raise e

    # --------------------------------------------------------------------------
    # Helper methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Scan the source_paths list for files with certain extensions
    # --------------------------------------------------------------------------
    def _get_source_files(self) -> dict[str, list[Path]]:
        """
        Scan the source_paths list for files with certain extensions.

        This method converts the clangs dict:

            {
                "Python": [".py"],
                "Glade": [".ui", ".glade"],
                "Desktop": [".desktop"],
            }

        into a dictionary of file paths to scan for each clang:

            {
                "Python": [<Path>/source.py, ...],
                "Glade": [<Path>/gui.ui, ...],
                "Desktop": [<Path>/template.desktop, ...],
            }

        so they can be passed to xgettext.

        Returns:
            A dictionary of file paths for each clang.
        """

        # we will eventually return a new dict
        dict_res = {}

        # ----------------------------------------------------------------------

        # for each clang name / list of exts
        for clang, exts in self._dict_clangs.items():

            # get res list for clang
            dict_res[clang] = []

            # add globs here for recursive search
            # NB: we already fixed dot in __init__
            glob_exts = [f"**/*{ext}" for ext in exts]

            # for each item in source_paths
            for src in self._list_sources:

                # src is dir
                if src.is_dir():

                    # for each clang ext
                    for glob_ext in glob_exts:

                        # get matching files and add to list
                        glob_res = list(
                            src.glob(glob_ext, case_sensitive=False)
                        )

                        # update result lang's val
                        dict_res[clang].extend(glob_res)

                # src is file
                elif src.is_file():

                    # check ext
                    for ext in exts:
                        if src.suffix == ext:
                            # update result lang's val
                            dict_res[clang].append(src)
                            break

        # ----------------------------------------------------------------------

        # remove duplicates from each res list
        # NB: user may specify dir and file in dir
        for clang, paths in dict_res.items():
            dict_res[clang] = list(set(paths))

        # prune final desktop if present
        if self._path_desk_out:
            for clang, paths in dict_res.items():
                if self._path_desk_out in paths:
                    paths.remove(self._path_desk_out)

        # ----------------------------------------------------------------------
        # return the final result
        return dict_res

    # --------------------------------------------------------------------------
    # Fix the list of po files by re-scanning the po dir
    # --------------------------------------------------------------------------
    def _get_po_files(self) -> list[Path]:
        """
        Fix the list of po files by re-scanning the po dir.

        This function returns a list of valid .po files in the po directory. It
        also attempts to fix the filenames by using the "Language" attribute
        inside the file if it is not already the filename.

        Returns:
            The list of .po files.
        """

        # ----------------------------------------------------------------------

        # fix up list_po every time main is run
        glob_po = f"**/*{self._S_EXT_PO}"
        list_res = list(self._path_po.glob(glob_po, case_sensitive=False))

        # ----------------------------------------------------------------------

        # for each po file
        for file_po in list_res:

            # get wlang name
            wlang = self._get_wlang_from_file(file_po)

            # check for no lang
            if not wlang:

                # warn, but do not fail
                F.printc(
                    self._S_WARN_NO_LANG.format(file_po),
                    fg=F.C_FG_YELLOW,
                    bold=True,
                )
                continue

            # check file name
            if file_po.stem != wlang:
                new_file_po = file_po.parent / f"{wlang}{self._S_EXT_PO}"
                file_po.rename(new_file_po)

        # ----------------------------------------------------------------------

        # fix up list_po after possible rename
        list_res = list(self._path_po.glob(glob_po, case_sensitive=False))

        # return final list of po files
        return list_res

    # --------------------------------------------------------------------------
    # Set up the initial file structure
    # --------------------------------------------------------------------------
    def _make_file_struct(self):
        """
        Set up the initial file structure.

        Seriously. That's it.
        """

        # make dirs
        self._path_i18n.mkdir(parents=True, exist_ok=True)
        self._path_locale.mkdir(parents=True, exist_ok=True)
        self._path_po.mkdir(parents=True, exist_ok=True)

        # NB: mucking with the location string makes weird shit happen
        # so just start with an empty file every time
        self._path_pot.unlink(missing_ok=True)

        # create a new, empty .pot file if it does not exist
        # NB: this allow us to use the -j flag without error (which would
        # happen if the initial file does not exist)
        self._path_pot.touch()

    # --------------------------------------------------------------------------
    # Get language code from inside file
    # --------------------------------------------------------------------------
    def _get_wlang_from_file(self, file_po: Path) -> str:
        """
        Get language code from inside file.

        Get the language code inside the file and use that to determine
        language (rather than the file name).

        Args:
            file_po: Path to the language file inside po folder.

        Returns:
            The language string inside the file, or an empty string.
        """

        # open file and get contents
        with open(file_po, encoding=self._S_DEF_ENCODING) as a_file:
            text = a_file.read()

        # find regex match and set result
        str_pattern = self._R_LANG_SCH
        res = re.search(str_pattern, text)
        if res:
            return res.group(2)

        # return default
        return ""

    # --------------------------------------------------------------------------
    # Check if any files contain empty translation strings
    # --------------------------------------------------------------------------
    def _check_empty_trans(self, clang_files):
        """
        Check if any files contain empty translation strings.

        Search each file in the clangs_file list to see if any of them contain
        an empty translation string (i.e. _("")) and warn with the file name
        and line number. Empty translation strings are reserved for xgettext
        use and will mess up your .pot file's header. Only supports Python
        files.

        Args:
            clang_files: The list of files to search.
        """

        # TODO: doesn't handle multi-line docstrings
        # do read(), replace triple matches with ""
        # save text to tmp file
        # then split into lines to look for split

        # TODO: also doesn't handle desktop or gui files

        # scan every file for _("") or _('')
        for item in clang_files:

            # get lines as list
            with open(item, encoding=self._S_DEF_ENCODING) as a_file:
                lines = a_file.readlines()

            # for each line
            for index, line in enumerate(lines):

                # only care about code portion
                res_split = F.split_line(line)
                code = res_split[0]

                # no code, don't care
                if not code:
                    continue

                # find empty translation
                res = re.search(self._R_EMPTY_SCH, code)

                #  found empty
                if res:

                    # warn, but do not fail
                    F.printc(
                        self._S_WARN_EMPTY_TRANS.format(item, index + 1),
                        fg=F.C_FG_YELLOW,
                        bold=True,
                    )

    # --------------------------------------------------------------------------
    # Set the header values for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self):
        """
        Set the header values for the pot which will carry over to each po.
        """

        # open file and get contents
        with open(self._path_pot, encoding=self._S_DEF_ENCODING) as a_file:
            text = a_file.read()

        # replace SOME DESCRIPTIVE TITLE.
        str_pattern = self._R_TITLE_SCH
        str_rep = self._R_TITLE_REP.format(self._str_domain)
        text = re.sub(str_pattern, str_rep, text)

        # replace copyright holder
        if self._str_author:
            str_pattern = self._R_COPY_SCH
            year = date.today().year
            str_rep = self._R_COPY_REP.format(year, self._str_author)
            text = re.sub(str_pattern, str_rep, text)

        # replace first author email
        if self._str_email:
            str_pattern = self._R_AUTH_SCH
            year = date.today().year
            str_rep = self._R_AUTH_REP.format(self._str_email, year)
            text = re.sub(str_pattern, str_rep, text)

        # make all locations relative to project dir
        rep = str(self._path_project) + "/"
        text = text.replace(rep, "")

        # save file
        with open(
            self._path_pot, "w", encoding=self._S_DEF_ENCODING
        ) as a_file:
            a_file.write(text)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # get path to test folder so we can test in-situ
    DIR_START = Path(__file__).parents[1].resolve()  # "CNLib"
    # PRJ_PATH = DIR_START / "tests/cnpot_test"

    # create an object
    try:
        potpy = CNPotPy(
            # ------------------------------------------------------------------
            # input
            #
            # project_path (ALL OTHER REL PATHS REL TO THIS!!!)
            # NB: if you pass "" or ".", use cwd
            # if you pass a rel path, it is resolved against cwd
            # if it is abs, use as-is
            # project_path=None,
            # project_path=Path(""),  # CNLib
            # project_path=Path("."),  # CNLib
            project_path=DIR_START,
            # project_path=Path("tests/cnpot_test"),
            # project_path=Path("tests/foo"),
            # project_path=DIR_START,
            # project_path=PRJ_PATH,

            # NB: to scan ALL of project_path, use default, or None, or []
            # source_paths=,
            # source_paths=None,
            # source_paths=[],
            # source_paths=[Path("src/python/source.py")],
            # source_paths=[Path("src/python/foo")],
            # source_paths=[PRJ_PATH],
            #
            # clangs_dict=,
            # clangs_dict=None,
            # clangs_dict={},
            # clangs_dict={"Foo": ["bar"]},
            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            # output
            # i18n_path=,
            # i18n_path=None,
            # i18n_path="",
            # i18n_path="i18n2"  # rel to project_path
            # i18n_path=PRJ_PATH / "i18n2",  # abs or rel to project_path

            # locale_name=,
            # locale_name=None,
            # locale_name="",
            # locale_name="locale2",  # name of folder under i18n

            # po_name=,
            # po_name=None,
            # po_name="",
            # po_name="po2",  # name of folder under i18n

            # domain=,
            # domain=None,
            # domain="",
            # domain="cnlib2",

        # ------------------------------------------------------------------
            # meta
            # ------------------------------------------------------------------
            # version=,
            # version=None,
            # version="",
            # version="1.2.3",

            # author=",
            # author=None,
            # author=",
            # author="cyclopticnerve2",

            # email=,
            # email=None,
            # email="",
            # email="cyclopticnerve2@gmail.com",

            # NB: None = no comments, "" = all comments, "<tag>" = comments
            # that contain tag
            # tag=,
            # tag=None,
            # tag="",
            # tag="i18n",
            # tag="I18N",

            # ------------------------------------------------------------------
            # desktop stuff
            # NB: paths must be absolute or relative to project_path
            # desk_in_path=Path("src/desktop/template.desktop"),
            # desk_out_path=Path("src/desktop/cnpot_test.desktop"),
        )

        potpy.main()

    # init throws error if project_path is not abs or not exist
    except ValueError as e:
        F.printc(e, fg=F.C_FG_RED, bold=True)

    # main raises OSError if xgt not found
    except OSError as e:
        print(e)

    # main raises CNRunError if any step fails
    except F.CNRunError as e:
        print(e)

# yes, or no and why
# has a different meaning than
# yes or no, and why
#
# the first one is equivalent to
# yes | (no & why)
# vs
# (yes | no) & why

# -)
