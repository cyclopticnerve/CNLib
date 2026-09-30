# ------------------------------------------------------------------------------
# Package :CNLib                                                  /          \
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

# TODO: __new__: type hints for params and ret val
# TODO: __init__: document source_paths
# TODO: __init__: document methods

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

    # commands

    # check if xgettext is installed
    _S_CMD_WHICH_XGT = "which xgettext"
    # call xgettext
    # NB: format params are... see below
    _S_CMD_XGT = (
        "xgettext "  # call GNU tool
        "--package-name={} "  # fix license string (param is self._domain)
        "-F "  # sort entries by file
        "-j "  # merge with existing file
        "-c{} "  # stop backpedaling for comments (param is self._tag)
        "-o {} "  # output file (param is self._path_pot)
        "-L {} "  # language of file to be scanned (param is current clang)
        "{}"  # path(s) to src files (param is str_clang_files)
    )
    # shell commands to make po/mo
    # NB: format params are file_po and self._path_pot
    _S_CMD_MERGE_POS = "msgmerge --update --backup=none {} {}"
    # NB: format params are file_mo and file_po
    _S_CMD_MAKE_MOS = "msgfmt -o {} {}"
    # NB: dir (-d) must contain LINGUAS file
    # NB: LINGUAS must contain paths to .po files, relative to dir_po (no ext)
    # NB: format params are self._desk_in, self._desk_out, and self._po_path
    _S_CMD_DESK = "msgfmt --desktop --template={} -o {} -d {}"

    # dirs

    # fixed GNU dir under locale dir
    _S_DIR_LC = "LC_MESSAGES"

    # files

    # fixed GNU file to store all wlang names for .desktop files
    _S_FILE_LINGUAS = "LINGUAS"

    # exts

    # fixed GNU file extensions
    _S_EXT_POT = ".pot"
    _S_EXT_PO = ".po"
    _S_EXT_MO = ".mo"

    # errors

    # error message for project path is not absolute
    _S_ERR_ABS_PRJ = (
        "Project directory must be absolute path and it must exist"
    )
    _S_ERR_DESK_TMP = (
        # error message for desktop template is not absolute
        "Desktop template file must be absolute path and it must exist"
    )
    # error message for desktop output is not absolute
    _S_ERR_DESK_OUT = "Desktop output file path must be absolute"
    # error message for no xgettext
    _S_ERR_NO_XGT = "No xgettext, use 'sudo apt install gettext'"
    # error message for no lang in po file
    # NB: format param is file name
    _S_ERR_NO_LANG = "No language set in po file: {}"
    # error for empty string
    # NB: format param is file name
    _S_ERR_EMPTY_TRANS = "Empty translation value: {}"
    # fixed strings for error messages
    _S_ERR_DOMAIN = "No domain"
    _S_ERR_I18N_DIR = "i18n_path must be an absolute Path"

    # defaults of my personal choosing (deal with it)

    # default tag (also a param)
    _S_TAG = "I18N"

    # default encoding for .pot and .po files (also a param)
    _S_ENCODING = "UTF-8"

    # default base folder for all i18n stuff (under prj)
    _S_DIR_I18N = "i18n"
    # default name of locale dir (under i18n_path)
    _S_DIR_LOCALE = "locale"
    # def dir name for user-editable translations (under i18n_path)
    _S_DIR_PO = "po"

    # --------------------------------------------------------------------------
    # Regex strings
    # --------------------------------------------------------------------------

    # title
    _R_TITLE_SCH = r"# SOME DESCRIPTIVE TITLE."
    # NB: format param is __PRJ_NAME_SMALL__
    _R_TITLE_REP = r"# {} translation template"

    # copyright
    _R_COPY_SCH = (
        r"(# Copyright \(C\) )(YEAR)( )(THE PACKAGE'S COPYRIGHT HOLDER)"
    )
    # NB: format params are year and author param
    _R_COPY_REP = r"\g<1>{}\g<3>{}"

    # email
    _R_EMAIL_SCH = r"(# FIRST AUTHOR )(<EMAIL@ADDRESS>)(, )(YEAR)"
    # NB: format params are email param and year
    _R_EMAIL_REP = r"\g<1>{}\g<3>{}"

    # project version
    _R_VER_SCH = r"(\"Project-Id-Version: )(.*?)(\\n\")"
    # NB: format param is version param
    _R_VER_REP = r"\g<1>{}\g<3>"

    # bugs email
    _R_BUGS_SCH = r"(\"Report-Msgid-Bugs-To: )(.*?)(\\n\")"
    # NB: format param is email param
    _R_BUGS_REP = r"\g<1>{}\g<3>"

    # charset
    _R_CHAR_SCH = r"(\"Content-Type: text/plain; charset=)(CHARSET)(.*)"
    # NB: format param is charset param
    _R_CHAR_REP = r"\g<1>{}\g<3>"

    # wlang
    _R_LANG_SCH = r"(\"Language: )(.*?)(\\n\")"

    # empty translation string (borks .pot output)
    _R_EMPTY_SCH = r"^[^#]*_\([\"|'] *[\"|']\)"

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

    _O_INST = None

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Create a new object from a class
    # --------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        Create a new object from a class.

        This is the usual implementation of a singleton class in Python.

        Args:
            cls: The class name/type/??? of the object to create.
            *args: A list of all the positional arguments to the class' creator
            function.
            **kwargs: A dictionary of all the keyword arguments to the class'
            creator function.

        Returns:
            An new or existing object of the specified class.
        """

        # this is our first instance
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
        # input
        # start dir (for relative paths)
        project_path: Path,
        # list of input folders/files (abs/rel Path)
        source_paths: list[Path] | None = None,
        # set clangs (override default, NOT combine)
        clangs: dict[str, list[str]] | None = None,
        # output
        # output dir
        i18n_path: Path | None = None,
        # locale dir under output dir
        locale_path: Path | None = None,
        # po dir under output dir
        po_path: Path | None = None,
        # meta
        # .mo file name
        domain: str | None = None,
        # project version
        version: str | None = None,
        # project author
        author: str | None = None,
        # project author email
        email: str | None = None,
        # tag to stop regressive context search
        tag: str | None = None,
        # file encoding
        encoding: str | None = None,
        # desktop stuff
        # path to template desktop
        desk_in_path: Path | None = None,
        # path to final desktop
        desk_out_path: Path | None = None,
    ):
        """
        Initialize the new object.

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.

        Args:
            project_path: The main project dir Path, used for relative paths.
                This Path must be absolute.
            i18n_path: The directory to place all i18n folders/files. Can be
                relative or absolute. A relative path is resolved against
                project_path. (default: None, use project_path / _S_DIR_I18N)
            source_paths:
                # TODO: more info
            domain: The name of the domain (program name). This name should
                be unique to you program. (default: None, use project_path.name)
            version: Version info to use in .pot/.po header. (default: None,
                do not replace)
            author: Author name to use in .pot/.po header. (default: None, do
                not replace)
            email: Email to use in .pot/.po header. (default: None, do not
                replace)
            tag: Tag that starts a context comment. If this string is
                empty, all comments above the string are included as context,
                until a blank or non-comment line is found. (default: None, use
                _S_TAG)
            encoding: The charset to use as the default in the .pot file, and
                any initial .po files created. (default: None, use _S_ENCODING)
            clangs: The dictionary of file extensions to scan for each
                clang. For each entry, the key is a clang known to xgettext.
                The value is a list of file extensions associated with that
                clang. If ths dict is empty, no files will be scanned.
                (default: _D_CLANGS)
            desk_in_path: The path to the desktop template file. Can be absolute
                or relative to project_path. (default: None, do not use)
            desk_out: The path to the desktop output file. Can be absolute
                or relative to project_path. (default: None, do not use)

        # TODO: document methods

        Raises:
            ValueError: If project_path is not absolute

        """

        # sanitize all params

        # ----------------------------------------------------------------------

        # input

        # check project_path
        if (
            not project_path
            or not project_path.is_absolute()
            or not project_path.exists()
        ):
            raise ValueError(self._S_ERR_ABS_PRJ)
        self._project_path = project_path

        # check source_paths
        if not source_paths:
            source_paths = [self._project_path]
        source_paths = [
            item if item.is_absolute() else self._project_path / item
            for item in source_paths
        ]
        self._source_paths = source_paths

        # check clangs
        if not clangs:  # True if param is None or def or not present or {}
            clangs = self._D_CLANGS

        # add leading dot if necessary
        for clang, exts in clangs.items():

            # check for leading dot
            exts = [
                f".{ext}" if not ext.startswith(".") else ext for ext in exts
            ]
            clangs[clang] = exts

        # clangs is fixed, use it
        self._clangs = clangs

        # ----------------------------------------------------------------------

        # output

        # check i18n_path
        if not i18n_path:
            i18n_path = self._project_path / self._S_DIR_I18N
        if not i18n_path.is_absolute():
            i18n_path = self._project_path / i18n_path
        self._i18n_path = i18n_path

        # check locale path
        if not locale_path:
            locale_path = self._i18n_path / self._S_DIR_LOCALE
        if not locale_path.is_absolute():
            locale_path = self._i18n_path / locale_path
        self._locale_path = locale_path

        # check po path
        if not po_path:
            po_path = self._project_path / self._S_DIR_PO
        if not po_path.is_absolute():
            po_path = self._project_path / po_path
        self._po_path = po_path

        # ----------------------------------------------------------------------

        # meta

        # get domain
        if not domain:
            # use project name
            domain = self._project_path.name
        self._domain = domain

        # just store args as props
        self._version = version
        self._author = author
        self._email = email

        # NB: when testing strings, "if not foo" will return True if the string
        # is None or "".
        # "if foo is None" will return True if the string is None, but False if
        # the string is ""

        # get tag
        if tag is None:  # not "", only None
            tag = self._S_TAG
        self._tag = tag

        # get encoding
        if encoding is None:  # not "", only None
            encoding = self._S_ENCODING
        self._encoding = encoding

        # check desk_in_path
        if desk_in_path:
            if not desk_in_path.is_absolute():
                desk_in_path = self._project_path / desk_in_path
        self._desk_in_path = desk_in_path

        # check desk_out_path
        if desk_out_path:
            if not desk_out_path.is_absolute():
                desk_out_path = self._project_path / desk_out_path
        self._desk_out_path = desk_out_path

        # ----------------------------------------------------------------------

        # make refs to folder structure (but DO NOT create)
        self._path_pot = self._i18n_path / f"{self._domain}{self._S_EXT_POT}"
        self._file_mo = f"{self._domain}{self._S_EXT_MO}"
        self._file_linguas = self._po_path / self._S_FILE_LINGUAS

        # store files to search
        self._dict_files = {}

        # default list of po files
        self._list_po = []

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Return the underscore function
    # --------------------------------------------------------------------------
    def underscore(self) -> Callable[[str], str]:
        """
        Return the underscore function.

        Returns:
            The gettext method to be used in Python source files.
        """

        # fix locale (mostly for GUI)
        locale.setlocale(locale.LC_ALL, "")
        locale.bindtextdomain(self._domain, self._locale_path)

        # get a translation object
        translation = gettext.translation(
            self._domain, self._locale_path, fallback=True
        )

        # return translation object's gettext method
        # NB: do not use install() here, that would only put _ in this file's
        # namespace. we want it in the caller's namespace, so return the func!
        # it can then be imported in the caller
        return translation.gettext

    # --------------------------------------------------------------------------
    # Run the program and make or update the files
    # --------------------------------------------------------------------------
    def main(self):
        """
        Run the main method to make or update the files.

        The main method of the class, performing its steps. This method can
        (and should) be run, in Mayor Tweed's words, "early and often". You
        should run it every time a source file that contains i18n strings is
        added, edited, or deleted. The ideal scenario is to run it just before
        the repo is synced, so that the .pot file is synced.

        Raises:
            cnlib.cnfunctions.CNError: If xgettext is not found or fails
        """

        # sanity check for xgettext
        try:
            F.run(self._S_CMD_WHICH_XGT, capture_output=True)
        except F.CNRunError as e:
            raise e

        # TODO: don't like this, blacklist instead
        # but delete later in do_desktop

        # kill old final desktop to prevent scanning
        # if self._desk_out:
        #     self._desk_out.unlink(missing_ok=True)
        #     self._desk_out.parent.mkdir(parents=True, exist_ok=True)

        # fix up source_paths every time main is run
        self._dict_files = self._get_dict_files()
        F.pp(self._dict_files)

        # fix up po list every time main is run
        self._list_po = self._get_list_po()

        # ----------------------------------------------------------------------
        # do the steps

        try:

            # do some housekeeping (mostly file structure stuff)
            self._make_file_struct()

            # make new .pot file
            self._make_pot()

            # make po files for new langs, or new .po files for existing langs
            self._make_pos()

            # # make .mo files for all existing .po files
            self._make_mos()

            # make desktop if template present
            self._make_desktop()

        # check for error, let someone else handle it
        except F.CNRunError as e:
            raise e

    # what is the try/exc/why
    # and when to catch/raise/wrap
    # same as testing and stuff that i cant wrap my head around
    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Scan the source list for files with certain extensions
    # --------------------------------------------------------------------------
    def _get_dict_files(self) -> dict[str, list[Path]]:
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

        # TODO: need a way to ignore prj.desktop when scanning

        # we will eventually return a new dict
        dict_res = {}

        # ----------------------------------------------------------------------

        # for each clang name / list of exts
        for clang, exts in self._clangs.items():

            # get res list for clang
            dict_res[clang] = []

            # for each item in source_paths
            for src in self._source_paths:

                # sanity check (we may list source_paths that don't exist yet)
                if not src.exists():
                    continue

                # src is dir
                if src.is_dir():
                    # add globs here for dir search
                    # NB: we already fixed dot in __init__
                    glob_exts = [
                        f"**/*{ext}" if not ext.startswith("**/*") else ext
                        for ext in exts
                    ]

                    # for each clang ext
                    for glob_ext in glob_exts:

                        # get matching files and add to list
                        glob_res = list(
                            src.glob(glob_ext, case_sensitive=False)
                        )

                        # update result lang's val
                        dict_res[clang].extend(glob_res)

                # src is file
                else:

                    # file, check ext
                    for ext in exts:
                        if src.suffix == ext:
                            dict_res[clang].append(src)

        # ----------------------------------------------------------------------
        # remove duplicates from each res list

        for clang, paths in dict_res.items():
            dict_res[clang] = list(set(paths))

        # ----------------------------------------------------------------------
        # return the final result
        return dict_res

    # --------------------------------------------------------------------------
    # Fix the list of po files by re-scanning po dir
    # --------------------------------------------------------------------------
    def _get_list_po(self):
        """
        Fix the list of po files by re-scanning po dir
        """

        res_list = []
        # fix up list_po every time main is run
        glob_po = f"**/*{self._S_EXT_PO}"
        res_list = list(self._po_path.glob(glob_po, case_sensitive=False))

        # also look for pot files
        glob_pot = f"**/*{self._S_EXT_POT}"
        list_pot = list(self._po_path.glob(glob_pot, case_sensitive=False))
        res_list.extend(list_pot)

        # for each po file
        for file_po in res_list:

            # get wlang name
            wlang = self._get_wlang_from_file(file_po)

            # check for no lang
            if not wlang:
                print(self._S_ERR_NO_LANG.format(file_po))
                continue

            # check file name
            if file_po.stem != wlang or file_po.suffix == self._S_EXT_POT:
                parent_po = file_po.parent
                new_file_po = parent_po / f"{wlang}{self._S_EXT_PO}"
                file_po.rename(new_file_po)

        # fix up list_po after possible rename
        glob_po = f"**/*{self._S_EXT_PO}"
        res_list = list(self._po_path.glob(glob_po, case_sensitive=False))

        return res_list

    # --------------------------------------------------------------------------
    # Do the basics of setting up i18n for a project
    # --------------------------------------------------------------------------
    def _make_file_struct(self):
        """
        Do the basics of setting up i18n for a project
        """

        # ----------------------------------------------------------------------
        # housekeeping

        # make dirs
        self._i18n_path.mkdir(parents=True, exist_ok=True)
        self._locale_path.mkdir(parents=True, exist_ok=True)
        self._po_path.mkdir(parents=True, exist_ok=True)

        # delete the existing .pot file (if it exists)
        self._path_pot.unlink(missing_ok=True)

        # create a new, empty .pot file if it does not exist
        # NB: this allow us to use the -j flag without error (which would
        # happen if the current file to join does not exist)
        self._path_pot.touch(exist_ok=True)

    # --------------------------------------------------------------------------
    # Create a .pot file in the pot folder
    # --------------------------------------------------------------------------
    def _make_pot(self):
        """
        Create a .pot file in the pot folder

        Raises:
            cnlib.cnfunctions.CNRunError: If the make fails

        Parses the files for each clang, creating a unified .pot file, which is
        placed in "<dir_pot>/<domain>.pot".
        """

        # for each clang name / list of clang files
        for clang_name, clang_files in self._dict_files.items():

            # sanity check
            if not clang_name or len(clang_files) == 0:
                continue

            # convert list of paths to quoted string
            list_clang_files = [f"{str(item)}" for item in clang_files]
            str_clang_files = " ".join(list_clang_files)

            # scan every file for _("") or _('')
            for item in list_clang_files:
                with open(item, encoding=self._S_ENCODING) as a_file:
                    text = a_file.read()
                    res = re.search(self._R_EMPTY_SCH, text)
                    if res:
                        print(self._S_ERR_EMPTY_TRANS.format(item), res)

            # get the cmd
            cmd = self._S_CMD_XGT.format(
                self._domain,
                self._tag,
                f'"{str(self._path_pot)}"',
                clang_name,
                str_clang_files,
            )

            # do the final command
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

        # fix short desc/copyright/email/version/charset in pot
        self._fix_pot_header()

    # --------------------------------------------------------------------------
    # Helper functions
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Merge any .po files in the po folder with new/existing .pot file
    # --------------------------------------------------------------------------
    def _make_pos(self):
        """
        Merge any .po files in the po folder with new/existing .pot file

        Raises:
            cnlib.cnfunctions.CNRunError: If the update fails

        Whenever a new .pot file is generated using _make_pot, this method will
        produce a new .po file for each wlang that contains the difference
        between the new .pot file and the existing .po file.

        This new .po file should be sent to the translator for each wlang. Then
        when the translator sends back the translated .po file, place it in the
        appropriate dir. Then run potpy.main to create a new .mo file.
        """

        # for each wlang in the po folder
        for file_po in self._list_po:

            # update existing po file using latest pot
            cmd = self._S_CMD_MERGE_POS.format(file_po, self._path_pot)
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

    # --------------------------------------------------------------------------
    # Create .mo files for all .po files in the locale folder
    # --------------------------------------------------------------------------
    def _make_mos(self):
        """
        Create .mo files for all .po files

        Raises:
            cnlib.cnfunctions.CNRunError if the make fails

        Makes all the required .mo files for all the .po files in the po dir
        """

        # for each wlang
        for file_po in self._list_po:

            # get .mo file (output)
            dir_mo = self._locale_path / file_po.stem / self._S_DIR_LC

            # nuke old mo/recreate
            if dir_mo.exists():
                shutil.rmtree(dir_mo)
            dir_mo.mkdir(parents=True, exist_ok=True)
            file_mo = dir_mo / self._file_mo

            # do the command
            cmd = self._S_CMD_MAKE_MOS.format(file_mo, file_po)
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

    # --------------------------------------------------------------------------
    # Localize the desktop file using all available pos
    # --------------------------------------------------------------------------
    def _make_desktop(self):  # , dt_template: Path, dt_out: Path):
        """
        Localize the desktop file using all available pos

        Arguments:
            dt_template: File containing the default information to include in
            the desktop file. This is the file that we use as a template when
            modifying metadata. This Path must be absolute.
            dt_out: Location of the i18n'ed desktop file. This is the file that
            will be distributed with your app. This Path must be absolute, but
            the file does not need to exist (if it does, it will be
            overwritten).

        Raises:
            OSError: If template Path is None or not absolute or does not exist
            OSError: if output Path is None or not absolute
            cnlib.cnfunctions.CNRunError: If the make fails

        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final .desktop file.
        """

        # sanity check
        if not self._desk_in_path:
            return

        if (
            not self._desk_in_path.is_absolute()
            or not self._desk_in_path.exists()
        ):
            raise OSError(self._S_ERR_DESK_TMP)
        # if not dt_out or not dt_out.is_absolute():
        #     raise OSError(self._S_ER_R_DESK_OUT)

        # # kill old final desktop to prevent scanning
        # if self._desk_out:
        #     self._desk_out.unlink(missing_ok=True)
        #     self._desk_out.parent.mkdir(parents=True, exist_ok=True)

        # update pot/po with strings from .desktop file
        # self.main()

        # write the LINGUAS file

        # get rel paths to all po files as strings
        # NB: self_list_po recalculated on run main
        list_po_str = [
            str(item.relative_to(self._po_path)) for item in self._list_po
        ]

        # remove exts from all po files
        list_po_lang = [
            item.removesuffix(self._S_EXT_PO) for item in list_po_str
        ]

        # make all entries into one long space separated string
        str_linguas = " ".join(list_po_lang)

        # write to linguas file
        with open(self._file_linguas, "w", encoding=self._S_ENCODING) as f:
            f.write(str_linguas)

        # do the thing
        cmd = self._S_CMD_DESK.format(
            self._desk_in_path, self._desk_out_path, self._po_path
        )
        try:
            F.run(cmd, shell=True, capture_output=True)
        except F.CNRunError as e:
            raise e

    # --------------------------------------------------------------------------
    # Set the header values for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self):
        """
        Set the header values for the pot which will carry over to each po
        """

        # open file and get contents
        with open(self._path_pot, encoding=self._S_ENCODING) as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = self._R_TITLE_SCH
        str_rep = self._R_TITLE_REP.format(self._domain)
        text = re.sub(str_pattern, str_rep, text)

        # replace version number
        if self._version != "":
            str_pattern = self._R_VER_SCH
            str_rep = self._R_VER_REP.format(self._version)
            text = re.sub(str_pattern, str_rep, text)

        # replace copyright (author)
        if self._author != "":
            str_pattern = self._R_COPY_SCH
            year = date.today().year
            str_rep = self._R_COPY_REP.format(year, self._author)
            text = re.sub(str_pattern, str_rep, text)

        # replace email
        if self._email != "":
            str_pattern = self._R_EMAIL_SCH
            year = date.today().year
            str_rep = self._R_EMAIL_REP.format(self._email, year)
            text = re.sub(str_pattern, str_rep, text)

            str_pattern = self._R_BUGS_SCH
            str_rep = self._R_BUGS_REP.format(self._email)
            text = re.sub(str_pattern, str_rep, text)

        # fix charset
        str_pattern = self._R_CHAR_SCH
        str_rep = self._R_CHAR_REP.format(self._encoding)
        text = re.sub(str_pattern, str_rep, text)

        # make all locations relative to project dir
        rep = str(self._project_path) + "/"
        text = text.replace(rep, "")

        # save file
        with open(self._path_pot, "w", encoding=self._S_ENCODING) as a_file:
            a_file.write(text)

    # --------------------------------------------------------------------------
    # Get language code from inside file
    # --------------------------------------------------------------------------
    def _get_wlang_from_file(self, file_po: Path) -> str:
        """
        Get language code from inside file

        Arguments:
            file_po: Path to the language file inside po folder

        Returns:
            The language string inside the file, or None

        Get the language code inside the file and use that to determine
        language (rather than the file name).
        """

        # open file and get contents
        with open(file_po, "r", encoding=self._S_ENCODING) as a_file:
            text = a_file.read()

        # find regex match and return
        str_pattern = self._R_LANG_SCH
        res = re.search(str_pattern, text)
        if res:
            lang = res.group(2)
            if len(lang):
                return res.group(2)

        # no lang
        return ""


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # get some paths to test folder so we can test in-situ
    DIR_START = Path(__file__).parents[1].resolve()  # "CNLib"
    PRJ_PATH = DIR_START / "tests/cnpot_test"

    # create an object
    cnpot = CNPotPy(
        # input
        # project_path (start of all rel paths)
        # NB: if you want this to be cwd, pass Path("")
        project_path=PRJ_PATH,
        # NB: to scan ALL of project path, use None, or default, or []
        # to scan ALL prj dir and more, must include project_path or Path("")
        source_paths=[
            PRJ_PATH,
            Path("src/python/source.py"),
        ],
        clangs={},  # or None or don't use
        # output
        # ------------------------------------------------------------------------------
        i18n_path=PRJ_PATH / "i18n",  # abs or rel to project_path
        # i18n_path=Path("")
        locale_dir="locale",  # name of folder under i18n
        po_dir="po",
        # ------------------------------------------------------------------------------
        # meta
        domain="cnlib",
        version="0.0.1",
        author="cyclopticnerve",
        email="cyclopticnerve@gmail.com",
        tag="I18N",
        encoding="UTF-8",
        # desktop stuff
        desk_in_path=Path("src/desktop/template.desktop"),
        desk_out_path=Path("src/desktop/cnpot_test.desktop"),
    )

    cnpot.main()

# -)

# yes, or no and why
# has a different meaning than
# yes or no, and why
#
# the first one is equivalent to
# yes | (no & why)
# vs
# (yes | no) & why
