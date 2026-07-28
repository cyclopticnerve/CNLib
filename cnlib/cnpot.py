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

# local imports
import cnlib.cnfunctions as F

# ------------------------------------------------------------------------------
# Module constants
# ------------------------------------------------------------------------------

# TODO: test this
# I18N: error for no domain in underscore
S_ERR_DOMAIN = _("Error: no domain") # type: ignore
# I18N: error for no locale or not absolute
S_ERR_LOCALE = _("Error: locale_path must be absolute") # type: ignore

# ------------------------------------------------------------------------------
# Module functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Return the underscore function
# ------------------------------------------------------------------------------
def underscore(domain: str, locale_dir: Path):
    """
    Return the underscore function

    Arguments:
        domain: The name of the program (or other stable name)
        locale_dir: Path to the 'locale' folder (must be absolute)

    Raises:
        OSError: If the domain is None or empty
        OSError: If the locale_dir is None or not absolute

    A module-level method to create the underscore function (used by xgettext
    to scrape translatable strings).
    """

    # sanity check
    if not domain:
        raise OSError(S_ERR_DOMAIN)
    if not locale_dir or not locale_dir.is_absolute():
        raise OSError(S_ERR_LOCALE)

    # fix locale (mostly for GUI)
    locale.bindtextdomain(domain, locale_dir)

    # get a translation object
    translation = gettext.translation(domain, locale_dir, fallback=True)

    # return object's gettext as underscore
    # NB: do not use install() here, that would only put _ in this file's
    # namespace. we want it in the caller's namespace, so return the func!
    # it can then be inherited from there
    return translation.gettext


# get this module's i18n
P_DIR_PRJ = Path(__file__).parent.resolve()
_ = underscore("cnlib", P_DIR_PRJ / "i18n/locale")

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
        main: Run the program and make or update the files
        make_desktop: Localize the desktop file using all available wlangs

    This class provides methods to create .pot, .po, .mo, and .desktop files
    for internationalizing a Python or PyGObject project.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # this is the default subdir for GNU
    S_DIR_LC = "LC_MESSAGES"
    # the file to store all wlang/domain names for .desktop files
    S_FILE_LINGUAS = "LINGUAS"

    # default file extensions
    S_EXT_POT = ".pot"
    S_EXT_PO = ".po"
    S_EXT_MO = ".mo"

    # default i18n folder
    S_DIR_I18N = "i18n"
    # default folders (under dir_i18n)
    S_DIR_LOCALE = "locale"
    S_DIR_PO = "po"

    # default comment tag
    S_TAG = "I18N"  # p, def
    # default encoding for .pot and .po files
    S_ENCODING = "UTF-8"  # p, def

    # check if xgettext is installed
    S_CMD_WHICH_XGT = "which xgettext"
    # call xgettext
    # NB: params are... see below
    S_CMD_XGT = (
        "cd {}; "  # change to project dir for rel paths
        "xgettext "  # call GNU tool
        "--package-name {} "  # fix meta
        "--package-version {} "  # fix meta
        "--msgid-bugs-address {} "  # fix meta
        "-F "  # sort entries by file
        "-j "  # append existing file
        "-c{} "  # stop backpedaling for comments
        "-o {} "  # final name of output file (absolute or rel to cwd)
        "-L {} "  # language of file from clangs
        "{}" # list of quoted paths to src files for this clang
    )
    # NB: dir (-d) must contain LINGUAS file
    # NB: LINGUAS must contain paths to .po files, relative to itself
    # NB: format params are template file, po dir, and output file
    S_CMD_DESK = "msgfmt --desktop --template={} -d {} -o {} "
    # shell commands to make po/mo
    # NB: format params are file_po and file_pot
    S_CMD_MERGE_POS = "msgmerge --update {} {} --backup=none"
    # NB: format params are mo_file and wlang_po
    S_CMD_MAKE_MOS = "msgfmt -o {} {}"

    # I18N: error message for project path is not absolute
    S_ERR_ABS_PRJ = _("Error: Project directory must be absolute path")
    # I18N: error message for desktop path is not absolute
    S_ERR_ABS_DESK = _("Error: Desktop file must be absolute path")
    # I18N: error message for no xgettext
    S_ERR_NO_XGT = _("Error: No xgettext, use 'sudo apt install gettext'")
    # I18N: error message for no lang in po file
    # NB: format param is file name
    S_ERR_NO_LANG = _("Error: no language set in po file: {}")

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

    R_CHAR_SCH = r"(\"Content-Type: text/plain; charset=)(CHARSET)(.*)"
    # NB: format param is charset param
    R_CHAR_REP = r"\g<1>{}\g<3>"

    R_LANG_SCH = r"(\"Language: )(.*?)(\\n\")"

    # dicts
    D_CLANGS = {
        "Python": [
            ".py",
        ],
        "Glade": [
            ".ui",
            ".glade",
        ],
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
        dir_prj: Path,
        # in
        list_src: list[Path] | None=None,
        # out
        dir_i18n: Path | None=None,
        # optional in
        str_domain: str="",
        str_version: str="",
        str_author: str="",
        str_email: str="",
        # use defaults in this class
        str_tag: str=S_TAG,
        str_encoding: str=S_ENCODING,
        # append clangs
        dict_clangs: dict[str, list[str]]=D_CLANGS,
    ):
        """
        Initialize the new object

        Args:
            dir_prj: The main project dir Path, used for relative paths. This
            Path must be absolute.

            list_src: Where to look for input files. This can be a list of
            directory or file Paths. Entries can be relative or absolute.
            Relative paths are resolved against dir_prj. (default: None, use
            [dir_prj])

            dir_i18n: Directory to place all i18 folders / files. Can be
            relative or absolute. A relative path is resolved against dir_prj.
            (default: None, dir_prj / S_DIR_I18N)

            str_domain: The name of the domain (program name). This name should
            be unique to you program. (default: "", use dir_prj.name)
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
            clang. If ths dict is empty, all files with extensions
            known to xgettext will be scanned. (default: D_CLANGS)

        Raises:
            OSError: If dir_prj is not absolute

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.

        """

        # check base dir (required abs path)
        if not dir_prj.is_absolute():
            # BYE BYE!!!
            raise OSError(self.S_ERR_ABS_PRJ)
        self._dir_prj = dir_prj

        # check input props (required abs or rel to prj dir)
        if list_src is None:
            list_src = [self._dir_prj]
        self._list_src = list_src

        # check base of file structure
        if dir_i18n is None:
            dir_i18n = dir_prj / self.S_DIR_I18N
        if not dir_i18n.is_absolute():
            dir_i18n = dir_prj / dir_i18n
        self._dir_i18n = dir_i18n

        # get domain
        if not str_domain:
            # use project name
            str_domain = self._dir_prj.name
        self._str_domain = str_domain

        # just store args as props
        self._str_version = str_version
        self._str_author = str_author
        self._str_email = str_email
        self._str_tag = str_tag
        self._str_encoding = str_encoding

        # get clangs/wlangs
        self._dict_clangs = dict_clangs
        self._list_wlangs = []

        # make refs to folder structure (but DO NOT create)
        self._dir_pot = self._dir_i18n
        self._dir_locale = self._dir_i18n / self.S_DIR_LOCALE
        self._dir_po = self._dir_i18n / self.S_DIR_PO

        # make refs to files (but DO NOT create)
        self._file_pot = self._dir_pot / f"{self._str_domain}{self.S_EXT_POT}"
        # NB: relative
        self._file_mo = f"{self._str_domain}{self.S_EXT_MO}"
        self._file_linguas = self._dir_po / self.S_FILE_LINGUAS

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

        # TODO: test this
        # check for xgettext
        try:
            cp = F.run(self.S_CMD_WHICH_XGT, capture_output=True)
            if not cp.stdout:
                raise OSError(self.S_ERR_NO_XGT)

        # check for error, let someone else handle it
        except F.CNRunError as e:
            raise e

        # ----------------------------------------------------------------------
        # do the steps

        try:

            # do some housekeeping (mostly file structure stuff)
            self._housekeeping()

            # make new absolute .pot file
            self._make_pot()

            # # make po files for new langs, or new .po files for existing langs
            self._update_pos()

            # # make sure all necessary dirs exist
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

        Args:
            dt_template: File containing the default information to include in
            the desktop file. This is the file that we use as a template when
            modifying metadata. This Path must be absolute.
            dt_out: Location of the i18n'ed desktop file. This is the file that
            will be distributed with your app. This Path must be absolute.

        Raises:
            OSError: If template od output path is not absolute
            cnlib.cnfunctions.CNRunError: If the make fails

        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final .desktop file.
        """

        # sanity check
        if not dt_template or not dt_template.is_absolute():
            raise OSError(self.S_ERR_ABS_DESK)
        if not dt_out or not dt_out.is_absolute():
            raise OSError(self.S_ERR_ABS_DESK)

        # kill old final desktop to prevent scanning
        dt_out.unlink(missing_ok=True)

        # update pot/po with strings from .desktop file
        self.main()

        # write the LINGUAS file
        linguas_path = self._dir_po / self.S_FILE_LINGUAS
        glob_po = f"**/*{self.S_EXT_PO}"
        list_pos = list(self._dir_po.glob(glob_po, case_sensitive=False))
        list_pos = [str(item.relative_to(self._dir_po)) for item in list_pos]

        # remove exts from all po files
        list_pos = [item.removesuffix(self.S_EXT_PO) for item in list_pos]
        linguas_str = " ".join(list_pos)
        with open(linguas_path, "w", encoding=self.S_ENCODING) as f:
            f.write(linguas_str)

        # check if template exists
        # NB: we do this last to make sure we create a linguas file, even if
        # there is no template
        if dt_template.exists():

            # build the command as a string
            cmd = self.S_CMD_DESK.format(dt_template, self._dir_po, dt_out)

            # run the command
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
    def _housekeeping(self):

        """
        Do the basics of setting up i18n for a project
        """

        # ----------------------------------------------------------------------
        # housekeeping

        # delete the existing .pot file (if it exists)
        self._file_pot.unlink(missing_ok=True)

        # create a new, empty .pot file if it does not exist
        # NB: this allow us to use the -j flag without error (which would
        # happen if the current file to join does not exist)
        self._file_pot.parent.mkdir(parents=True, exist_ok=True)
        self._file_pot.touch(exist_ok=True)

        # make file structure
        self._dir_locale.mkdir(parents=True, exist_ok=True)
        self._dir_po.mkdir(parents=True, exist_ok=True)

        # fix up list_src
        self._fix_list_src()

        # fix up dict_clangs
        self._fix_dict_clangs()

        # fix up list_wlangs
        self._fix_list_wlangs()


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

            # sanity checks
            if not clang_name or len(clang_files) == 0:
                continue

            # TODO: here is where empty args matter
            cmd = self.S_CMD_XGT.format(
                self._dir_prj,
                self._str_domain,
                self._str_version,
                self._str_email,
                self._str_tag,
                self._file_pot,
                clang_name,
                self._list_wlangs
            )

            # do the final command
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

        # fix short desc/copyright/email/version/charset in pot
        self._fix_pot_header()

    # --------------------------------------------------------------------------
    # Merge any .po files in the pos folder with existing .pot file
    # --------------------------------------------------------------------------
    def _update_pos(self):
        """
        Merge any .po files in the pos folder with existing .pot file

        Raises:
            cnlib.cnfunctions.CNRunError: If the make fails

        Whenever a new .pot file is generated using _make_pot, this method will
        produce a new .po file for each wlang that contains the difference
        between the new .pot file and the existing .po file.

        This new .po file should be sent to the translator for each wlang. Then
        when the translator sends back the translated .po file, place it in the
        appropriate dir. Then run potpy.main to create a new .mo file.
        """


        for item in list_pos:
            cmd = C_UPDATE.format(str(item), str(P_FILE_POT))
            subprocess.run(cmd, shell=True, check=True)

    # --------------------------------------------------------------------------
    # Create .mo files for all .po files in the locale folder
    # --------------------------------------------------------------------------
    def _make_mos(self):
        """
        Create .mo files for all .po files in the po folder

        Raises:
            cnlib.cnfunctions.CNRunError if the make fails

        Makes all the required .mo files for all the .po files in the po dir
        """

        # for each wlang
        for file_po in self._list_wlangs:

            # get wlang name
            wlang = self._get_wlang_from_file(file_po)
            if not wlang:
                print(self.S_ERR_NO_LANG.format(file_po))
                continue

            # get .mo file (output)
            mo_dir = self._dir_locale / str(wlang) / self.S_DIR_LC
            mo_dir.mkdir(parents=True, exist_ok=True)
            mo_file = mo_dir / self._file_mo

            # do the command
            cmd = self.S_CMD_MAKE_MOS.format(mo_file, file_po)
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Set the header values for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self):
        """
        Set the header values for the pot which will carry over to each po
        """

        # open file and get contents
        with open(self._file_pot, "r", encoding=self.S_ENCODING) as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = self.R_TITLE_SCH
        str_rep = self.R_TITLE_REP.format(self._str_domain)
        text = re.sub(str_pattern, str_rep, text)

        # replace copyright
        str_pattern = self.R_COPY_SCH
        year = date.today().year
        str_rep = self.R_COPY_REP.format(year, self._str_author)
        text = re.sub(str_pattern, str_rep, text)

        # replace email
        str_pattern = self.R_EMAIL_SCH
        email = self._str_email
        year = date.today().year
        str_rep = self.R_EMAIL_REP.format(email, year)
        text = re.sub(str_pattern, str_rep, text)

        # replace version number
        str_pattern = self.R_VER_SCH
        str_rep = self.R_VER_REP.format(self._str_version)
        text = re.sub(str_pattern, str_rep, text)

        # fix charset
        str_pattern = self.R_CHAR_SCH
        str_rep = self.R_CHAR_REP.format(self._str_encoding)
        text = re.sub(str_pattern, str_rep, text)

        # make all locations relative to project dir
        rep = str(self._dir_prj) + "/"
        text = text.replace(rep, "")

        # save file
        with open(self._file_pot, "w", encoding=self.S_ENCODING) as a_file:
            a_file.write(text)


    # --------------------------------------------------------------------------
    # Get language code from inside file
    # --------------------------------------------------------------------------
    # FIXME: type
    def _get_wlang_from_file(self, file_po):
        """    # FIXME: type
        Get language code from inside file

        Args:
            file_po: Path to the language file inside po folder

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

    # --------------------------------------------------------------------------
    # Scan the source dirs for files with certain extensions
    # --------------------------------------------------------------------------
    def _fix_list_src(self):
    # FIXME: type
        # TODO: where/how quoted? and check relative

    # first check if item in absolute
    #     if it is, add and contu=inut\
    # if not, try to make abs using dir_ptj
    # if not,???

        # get item is abs
        paths = [item.is_absolute() ? item : item = self.prj_dir / item for item in paths]
        paths = self._list_src
        paths = [f'"{item}"' for item in self._list_src]
        # scan subdirs, files, etc build list of all abs paths to sources
        return " ".join(paths)

    # --------------------------------------------------------------------------
    # Scan the source dirs for files with certain extensions
    # --------------------------------------------------------------------------
    # FIXME: type
    def _fix_dict_clangs(self):
        """
        Scan the source dirs for files with certain extensions

        Returns:
            A dictionary containing file paths to source files

        This method uses the list_src list to convert the dict_clangs
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

        # FIXME: merge new w/ D_CLANGS to get bare minimum
        # the dict to return
        dict_res = {}

        # ----------------------------------------------------------------------

        # for each item in list_src
        for place in self._list_src:

            # resolve place
            place = Path(place)
            if not place.is_absolute():
                place = self._dir_prj / place

            # check if dir
            if place.is_dir():

                # for each clang name / list of exts
                for clang, exts in self._dict_clangs.items():

                    # check for leading dot
                    exts = [
                        f".{ext}" if not ext.startswith(".") else ext
                        for ext in exts
                    ]

                    # the new list of files
                    list_clang = []

                    # for each clang ext
                    for ext in exts:

                        # get matching files and add to list
                        glob = f"**/*{ext}"
                        res = list(place.glob(glob, case_sensitive=False))
                        list_clang.extend(res)

                    # update result lang's val
                    # NB: xgettext does not handle Paths, only strs
                    list_clang = [str(item) for item in list_clang]
                    list_old = dict_res.get(clang, [])
                    list_old.extend(list_clang)
                    dict_res[clang] = list_old

            # src item is file
            else:

                # get item suffix (including dot)
                ext_place = place.suffix

                # find lang from suffix
                for clang, exts in self._dict_clangs.items():

                    # check for leading dot
                    exts = [
                        f".{ext}" if not ext.startswith(".") else ext
                        for ext in exts
                    ]

                    # if this item belongs to this clang
                    if ext_place in exts:

                        # update result lang's val
                        # NB: xgettext does not handle Paths, only strs
                        list_old = dict_res.get(clang, [])
                        list_old.extend([str(place)])
                        dict_res[clang] = list_old

                        break
            paths = [f'"{item}"' for item in clang_files]
            j_paths = " ".join(paths)
            cmd += j_paths
        # ----------------------------------------------------------------------

        # return the result
        return dict_res

    def _fix_list_wlangs(self):
        glob_po = f"**/*{self.S_EXT_PO}"
        self._list_wlangs = list(
            self._dir_po.glob(glob_po, case_sensitive=False)
        )
        # return self._list_wlangs
# -)

# yes, or no and why
# has a different meaning than
# yes or no, and why
#
# the first one is equivalent to
# yes | (no & why)
# vs
# (yes | no) & why
