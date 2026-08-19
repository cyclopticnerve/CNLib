# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnpot.py                                              |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
Run GNU gettext tools to create i18n files for a project

This class converts all marked strings in source files to i18n versions using
xgettext, and creates .po files in the locale directory. It also uses msgfmt
to convert .po files to .mo files.

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

# local imports
import cnlib.cnfunctions as F

# ------------------------------------------------------------------------------
# Module constants
# ------------------------------------------------------------------------------

S_ERR_DOMAIN = "No domain"
S_ERR_LOCALE = "locale_dir must be an absolute Path"

# ------------------------------------------------------------------------------
# Module functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Return the underscore function
# ------------------------------------------------------------------------------
def underscore(domain: str, locale_dir: Path) -> Callable[[str], str]:
    """
    Returns the underscore function

    Arguments:
        domain: Name of the program (or other stable name)
        locale_dir: Path to the 'locale' folder (must be absolute)

    Returns:
        The gettext method for the domain and locale_dir

    Raises:
        OSError: The domain is None or empty
        OSError: The locale_dir is None or not absolute

    A module method to create the underscore function (used by xgettext to
    scrape translatable strings).
    """

    # sanity check
    if not domain:
        raise OSError(S_ERR_DOMAIN)
    if not locale_dir or not locale_dir.is_absolute():
        raise OSError(S_ERR_LOCALE)

    # fix locale (mostly for GUI)
    locale.setlocale(locale.LC_ALL, "")
    locale.bindtextdomain(domain, locale_dir)

    # get a translation object
    translation = gettext.translation(domain, locale_dir, fallback=True)

    # return object's gettext as underscore
    # NB: do not use install() here, that would only put _ in this file's
    # namespace. we want it in the caller's namespace, so return the func!
    # it can then be inherited from there
    return translation.gettext

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to handle making the different I18N files needed for a Python project
# ------------------------------------------------------------------------------
class CNPotPy:
    """
    A class to handle making the different I18N files needed for a Python
    project

    Methods:
        main: The main method to make or update the folders/files
        make_desktop: Localize the desktop file using all available wlangs

    This class provides methods to create .pot, .po, .mo, and .desktop files
    for internationalizing a CLI or GUI project.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # this is the default subdir for GNU
    S_DIR_LC = "LC_MESSAGES"
    # the file to store all wlang names for .desktop files
    S_FILE_LINGUAS = "LINGUAS"

    # default file extensions
    S_EXT_POT = ".pot"
    S_EXT_PO = ".po"
    S_EXT_MO = ".mo"

    # default folders (under path_i18n)
    S_DIR_LOCALE = "locale"
    S_DIR_PO = "po"

    # default encoding for .pot and .po files
    S_ENCODING = "UTF-8"

    # check if xgettext is installed
    S_CMD_WHICH_XGT = "which xgettext"
    # call xgettext
    # NB: params are... see below
    S_CMD_XGT = (
        "xgettext "  # call GNU tool
        "--package-name={} "  # str_domain (fixes license string)
        "-F "  # sort entries by file
        "-j "  # merge with existing file
        "-c{} "  # stop backpedaling for comments (str_tag)
        "-o {} "  # final name of output file (absolute or rel to cwd)
        "-L {} "  # language of file from clangs
        "{}"  # list of quoted paths to src files for this clang
    )
    # NB: dir (-d) must contain LINGUAS file
    # NB: LINGUAS must contain paths to .po files, relative to dir_po (no ext)
    # NB: format params are template file, output file, and dir_po
    S_CMD_DESK = "msgfmt --desktop --template={} -o {} -d {}"
    # shell commands to make po/mo
    # NB: format params are file_po and file_pot
    S_CMD_MERGE_POS = "msgmerge --update --backup=none {} {}"
    # NB: format params are file_mo and file_po
    S_CMD_MAKE_MOS = "msgfmt -o {} {}"

    # error message for project path is not absolute
    S_ERR_ABS_PRJ = "Project directory must be absolute path"
    # error message for desktop template is not absolute
    S_ERR_DESK_TMP = (
        "Desktop template file must be absolute path and it must exist"
    )
    # error message for desktop output is not absolute
    S_ERR_DESK_OUT = "Desktop output file path must be absolute"
    # error message for no xgettext
    S_ERR_NO_XGT = "No xgettext, use 'sudo apt install gettext'"
    # error message for no lang in po file
    # NB: format param is file name
    S_ERR_NO_LANG = "No language set in po file: {}"
    # error for empty string
    # NB: format param is file name
    S_ERR_EMPTY_TRANS = "empty translation value: {}"

    # meta regexes
    R_TITLE_SCH = r"# SOME DESCRIPTIVE TITLE."
    # NB: format param is __PRJ_NAME_SMALL__
    R_TITLE_REP = r"# {} translation template"

    R_COPY_SCH = (
        r"(# Copyright \(C\) )(YEAR)( )(THE PACKAGE'S COPYRIGHT HOLDER)"
    )
    # NB: format params are year and author param
    R_COPY_REP = r"\g<1>{}\g<3>{}"

    R_EMAIL_SCH = r"(# FIRST AUTHOR )(<EMAIL@ADDRESS>)(, )(YEAR)"
    # NB: format params are email param and year
    R_EMAIL_REP = r"\g<1>{}\g<3>{}"

    R_VER_SCH = r"(\"Project-Id-Version: )(.*?)(\\n\")"
    # NB: format param is version param
    R_VER_REP = r"\g<1>{}\g<3>"

    R_BUGS_SCH = r"(\"Report-Msgid-Bugs-To: )(.*?)(\\n\")"
    # NB: format param is email param
    R_BUGS_REP = r"\g<1>{}\g<3>"

    R_CHAR_SCH = r"(\"Content-Type: text/plain; charset=)(CHARSET)(.*)"
    # NB: format param is charset param
    R_CHAR_REP = r"\g<1>{}\g<3>"

    R_LANG_SCH = r"(\"Language: )(.*?)(\\n\")"
    R_EMPTY_SCH = r"_\([\'\"]\s*[\'\"]\)"

    # dicts
    D_CLANGS = {
        "Python": [".py"],
        "Glade": [".ui", ".glade"],
        "Desktop": [".desktop"],
    }

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        # base prj dir
        path_prj: Path,
        # out
        path_i18n: Path, #| None = None,
        # in
        list_src: list[Path],
        # optional in
        str_domain: str = "",
        str_version: str = "",
        str_author: str = "",
        str_email: str = "",
        # use defaults for tag and encoding
        str_tag: str = "",#S_TAG,
        str_encoding: str = S_ENCODING,
        # append clangs
        dict_clangs: dict[str, list[str]] | None = None,
    ):
        """
        Initializes the new object

        Arguments:
            path_prj: The main project dir Path, used for relative paths. This
            Path must be absolute.

            list_src: Where to look for input files. This can be a list of
            directory or file Paths. Entries can be relative or absolute.
            Relative paths are resolved against path_prj. (default: None, use
            [path_prj])

            path_i18n: Directory to place all i18 folders / files. Can be
            relative or absolute. A relative path is resolved against path_prj.
            (default: None, use path_prj / S_DIR_I18N)

            str_domain: The name of the domain (program name). This name should
            be unique to you program. (default: "", use path_prj.name)
            str_version: Version info to use in .pot/.po header (default: "",
            do not replace)
            str_author: Author name to use in .pot/.po header (default: "", do
            not replace)
            str_email: Email to use in .pot/.po header (default: "", do not
            replace)

            str_tag: Tag that starts a context comment. If this string is
            empty, all comments before the string are included as context
            (default: S_TAG)
            str_encoding: the charset to use as the default in the .pot file,
            and any initial .po files created (default: S_ENCODING)

            dict_clangs: The dictionary of file extensions to scan for each
            clang. For each entry, the key is a clang known to xgettext. The
            value is a list of file extensions associated with that clang. If
            ths dict is empty, no files will be scanned. (default: D_CLANGS)

        Raises:
            OSError: If path_prj is not absolute

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.

        """

        # check prj_dir
        path_prj = Path(path_prj)
        if not path_prj.is_absolute() or not path_prj.exists():
            # BYE BYE!!!
            raise OSError(self.S_ERR_ABS_PRJ)
        self._path_prj = path_prj

        # check base of file structure
        path_i18n = Path(path_i18n)
        if not path_i18n.is_absolute():
            path_i18n = path_prj / path_i18n
        self._path_i18n = path_i18n

        # check list_src
        if list_src is None:
            list_src = [self._path_prj]
        list_src = [Path(item) for item in list_src]
        list_src = [
            item if item.is_absolute() else self._path_prj / item
            for item in list_src
        ]
        self._list_src = list_src

        # get domain
        if not str_domain:
            # use project name
            str_domain = self._path_prj.name
        self._str_domain = str_domain

        # just store args as props
        # NB: if blank, leave blank
        self._str_version = str_version
        self._str_author = str_author
        self._str_email = str_email
        self._str_tag = str_tag
        self._str_encoding = str_encoding

        # make refs to folder structure (but DO NOT create)
        self._path_locale = self._path_i18n / self.S_DIR_LOCALE
        self._path_po = self._path_i18n / self.S_DIR_PO

        # store clangs
        if dict_clangs is None:
            dict_clangs = self.D_CLANGS
        self._dict_clangs_in = dict_clangs
        self._dict_clangs = {}

        # default list of po files
        self._list_po = []

        # make refs to files (but DO NOT create)
        self._path_pot = (
            self._path_i18n / f"{self._str_domain}{self.S_EXT_POT}"
        )

        # NB: full path created at runtime
        self._file_mo = f"{self._str_domain}{self.S_EXT_MO}"
        self._file_linguas = self._path_po / self.S_FILE_LINGUAS

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the program and make or update the files
    # --------------------------------------------------------------------------
    def main(self):
        """
        Run the program and make or update the files

        Raises:
            OSError: If xgettext not found
            cnlib.cnfunctions.CNRunError: If anything fails

        Main method of the class, performing its steps. This method can (and
        should) be run, in Mayor Tweed's words, "early and often". You should
        run it every time a source file that contains i18n strings is added,
        edited, or deleted. The ideal scenario is to run it just before the
        repo is synced, so that the .pot file is synced.
        """

        # sanity check for xgettext
        try:
            cp = F.run(self.S_CMD_WHICH_XGT, capture_output=True)
            if not cp.stdout:
                raise OSError(self.S_ERR_NO_XGT)
        except F.CNRunError as e:
            raise e

        # fix up sources every time main is run (changes when making desktop)
        self._fix_dict_clangs()

        # fix up po list every time main is run (changes when pasting po files
        # with questionable names)
        self._fix_list_po()

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

        # check for error, let someone else handle it
        except F.CNRunError as e:
            raise e

    # --------------------------------------------------------------------------
    # Localize the desktop file using all available wlangs
    # --------------------------------------------------------------------------
    def make_desktop(self, dt_template: Path, dt_out: Path):
        """
        Localize the desktop file using all available wlangs

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
        if (
            not dt_template
            or not dt_template.is_absolute()
            or not dt_template.exists()
        ):
            raise OSError(self.S_ERR_DESK_TMP)
        if not dt_out or not dt_out.is_absolute():
            raise OSError(self.S_ERR_DESK_OUT)

        # kill old final desktop to prevent scanning
        dt_out.unlink(missing_ok=True)

        # update pot/po with strings from .desktop file
        self.main()

        # write the LINGUAS file

        # get rel paths to all po files as strings
        # NB: self_list_po recalculated on run main
        list_po_str = [
            str(item.relative_to(self._path_po)) for item in self._list_po
        ]

        # remove exts from all po files
        list_po_lang = [
            item.removesuffix(self.S_EXT_PO) for item in list_po_str
        ]

        # make all entries into one long space separated string
        str_linguas = " ".join(list_po_lang)

        # write to linguas file
        with open(self._file_linguas, "w", encoding=self.S_ENCODING) as f:
            f.write(str_linguas)

        # do the thing
        cmd = self.S_CMD_DESK.format(dt_template, dt_out, self._path_po)
        try:
            F.run(cmd, shell=True, capture_output=True)
        except F.CNRunError as e:
            raise e

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

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
        self._path_i18n.mkdir(parents=True, exist_ok=True)
        self._path_locale.mkdir(parents=True, exist_ok=True)
        self._path_po.mkdir(parents=True, exist_ok=True)

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
        placed in "<dir_pot>/<str_domain>.pot".
        """

        # for each clang name / list of clang files
        for clang_name, clang_files in self._dict_clangs.items():

            # sanity check
            if not clang_name or len(clang_files) == 0:
                continue

            # convert list of paths to quoted string
            list_clang_files = [f"{str(item)}" for item in clang_files]
            str_clang_files = " ".join(list_clang_files)

            # scan every file for _("") or _('')
            for item in list_clang_files:
                with open(item, encoding=self.S_ENCODING) as a_file:
                    text = a_file.read()
                    res = re.search(self.R_EMPTY_SCH, text)
                    if res:
                        print(self.S_ERR_EMPTY_TRANS.format(item))

            # get the cmd
            cmd = self.S_CMD_XGT.format(
                self._str_domain,
                self._str_tag,
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
            cmd = self.S_CMD_MERGE_POS.format(file_po, self._path_pot)
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
            dir_mo = self._path_locale / file_po.stem / self.S_DIR_LC

            # nuke old mo/recreate
            if dir_mo.exists():
                shutil.rmtree(dir_mo)
            dir_mo.mkdir(parents=True, exist_ok=True)
            file_mo = dir_mo / self._file_mo

            # do the command
            cmd = self.S_CMD_MAKE_MOS.format(file_mo, file_po)
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

    # --------------------------------------------------------------------------
    # Helper functions
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Scan the source dirs for files with certain extensions
    # --------------------------------------------------------------------------
    def _fix_dict_clangs(self):
        """
        Scan the source dirs for files with certain extensions

        Returns:
            A dictionary of file paths for each clang

        This method uses the list_src list to convert the _dict_clangs_in
        dictionary:
            {
                "Python": [".py"],
                "Glade": [".ui", ".glade"],
                "Desktop": [".desktop"],
            }
        into a dictionary of file paths to scan for each clang:
            {
                "Python": [<Path>, ...],
                "Glade": [<Path>, ...],
                "Desktop": [<Path>, ...],
            }
        so they can be passed to xgettext.
        """

        # reset dict when running main twice
        # NB: this is because we are looping through sources,
        # appending/extending the dict as we go, so need a fresh start each
        # time
        self._dict_clangs = {}

        # fix extensions
        for _clang, exts in self._dict_clangs_in.items():

            # check for leading dot
            exts = [
                f".{ext}" if not ext.startswith(".") else ext for ext in exts
            ]

        # ----------------------------------------------------------------------

        # for each item in list_src
        for src in self._list_src:

            # sanity check
            if not src.exists():
                continue

            # check if dir
            if src.is_dir():

                # for each clang name / list of exts
                for clang, exts in self._dict_clangs_in.items():

                    # default results
                    glob_res = []

                    # for each clang ext
                    for ext in exts:

                        # get matching files and add to list
                        glob = f"**/*{ext}"
                        glob_res = list(src.glob(glob, case_sensitive=False))

                    # update result lang's val
                    list_old = self._dict_clangs.get(clang, [])
                    list_old.extend(glob_res)
                    self._dict_clangs[clang] = list_old

            # src item is file
            else:

                # files are a one-shot
                found = False

                # find lang from suffix
                for clang, exts in self._dict_clangs_in.items():

                    # if this item belongs to this clang
                    for ext in exts:

                        # update result lang's val
                        if src.suffix == ext:
                            list_old = self._dict_clangs.get(clang, [])
                            list_old.append(src)
                            self._dict_clangs[clang] = list_old

                            # stop looking at this ext
                            found = True
                            break

                    # stop looking at this src
                    if found:
                        break

    # --------------------------------------------------------------------------
    # Fix the list of po files by re-scanning po dir
    # --------------------------------------------------------------------------
    def _fix_list_po(self):
        """
        Fix the list of po files by re-scanning po dir
        """

        # fix up list_po every time main is run
        glob_po = f"**/*{self.S_EXT_PO}"
        self._list_po = list(self._path_po.glob(glob_po, case_sensitive=False))

        # also look for pot files
        glob_pot = f"**/*{self.S_EXT_POT}"
        list_pot = list(self._path_po.glob(glob_pot, case_sensitive=False))
        self._list_po.extend(list_pot)

        # for each po file
        for file_po in self._list_po:

            # get wlang name
            wlang = self._get_wlang_from_file(file_po)

            # check for no lang
            if not wlang:
                print(self.S_ERR_NO_LANG.format(file_po))
                continue

            # check file name
            if file_po.stem != wlang or file_po.suffix == self.S_EXT_POT:
                parent_po = file_po.parent
                new_file_po = parent_po / f"{wlang}{self.S_EXT_PO}"
                file_po.rename(new_file_po)

        # fix up list_po after possible rename
        glob_po = f"**/*{self.S_EXT_PO}"
        self._list_po = list(self._path_po.glob(glob_po, case_sensitive=False))

    # --------------------------------------------------------------------------
    # Set the header values for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self):
        """
        Set the header values for the pot which will carry over to each po
        """

        # open file and get contents
        with open(self._path_pot, encoding=self.S_ENCODING) as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = self.R_TITLE_SCH
        str_rep = self.R_TITLE_REP.format(self._str_domain)
        text = re.sub(str_pattern, str_rep, text)

        # replace version number
        if self._str_version != "":
            str_pattern = self.R_VER_SCH
            str_rep = self.R_VER_REP.format(self._str_version)
            text = re.sub(str_pattern, str_rep, text)

        # replace copyright (author)
        if self._str_author != "":
            str_pattern = self.R_COPY_SCH
            year = date.today().year
            str_rep = self.R_COPY_REP.format(year, self._str_author)
            text = re.sub(str_pattern, str_rep, text)

        # replace email
        if self._str_email != "":
            str_pattern = self.R_EMAIL_SCH
            year = date.today().year
            str_rep = self.R_EMAIL_REP.format(self._str_email, year)
            text = re.sub(str_pattern, str_rep, text)

        # fix charset
        str_pattern = self.R_CHAR_SCH
        str_rep = self.R_CHAR_REP.format(self._str_encoding)
        text = re.sub(str_pattern, str_rep, text)

        # make all locations relative to project dir
        rep = str(self._path_prj) + "/"
        text = text.replace(rep, "")

        # save file
        with open(self._path_pot, "w", encoding=self.S_ENCODING) as a_file:
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
        with open(file_po, "r", encoding=self.S_ENCODING) as a_file:
            text = a_file.read()

        # find regex match and return
        str_pattern = self.R_LANG_SCH
        res = re.search(str_pattern, text)
        if res:
            lang = res.group(2)
            if len(lang):
                return res.group(2)

        # no lang
        return ""


# -)

# yes, or no and why
# has a different meaning than
# yes or no, and why
#
# the first one is equivalent to
# yes | (no & why)
# vs
# (yes | no) & why
