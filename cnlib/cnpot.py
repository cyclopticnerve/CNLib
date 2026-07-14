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
# Functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Return the underscore function
# ------------------------------------------------------------------------------
def underscore(domain, path):
    """
    Return the underscore function

    Arguments:
        domain: the name of the program (or other stable name)
        path: Path to the 'locale' folder (must be absolute)

    A module-level method to create the underscore function (used by xgettext
    to scrape translatable strings).
    """

    # in case we pass a Path object
    path = str(path)

    # fix locale (mostly for GUI)
    locale.bindtextdomain(domain, path)

    # get a translation object
    translation = gettext.translation(domain, path, fallback=True)

    # return object's gettext as underscore
    # NB: do not use install() here, that would only put _ in this file's
    # namespace. we want it in the caller's namespace, so return the func!
    # it can then be inherited from there
    return translation.gettext


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

    # default encoding for .pot and .po files
    S_ENCODING = "UTF-8"
    # this is the default subdir for GNU
    S_DIR_LC = "LC_MESSAGES"
    # the file to store all wlang/domain names for .desktop files
    S_FILE_LINGUAS = "LINGUAS"

    # default file extensions
    S_EXT_POT = ".pot"
    S_EXT_PO = ".po"
    S_EXT_MO = ".mo"

    S_CMD_WHICH_XGT = "which xgettext"
    # NB: dir (-d) must contain LINGUAS file
    # NB: LINGUAS must contain paths to .po files, relative to itself
    # NB: format params are po dir, template file, and output file
    S_CMD_DESK = "msgfmt --desktop --template={} -d {} -o {} "
    # shell commands to make po/mo
    # NB: format params are file_po and pot_file
    S_CMD_MERGE_POS = "msgmerge --update {} {} --backup=none"
    # NB: format params are mo_file and wlang_po
    S_CMD_MAKE_MOS = "msgfmt -o {} {}"

    S_ERR_NO_XGT = _("No xgettext, use 'sudo apt install gettext'")
    # error message for no lang in po file
    # NB: format param is file name
    S_ERR_NO_LANG = _("Error: no language set in po file: {}")

    # header regexes
    R_TITLE_SCH = r"# SOME DESCRIPTIVE TITLE."
    R_TITLE_REP = r"# {} translation template"

    R_COPY_SCH = (
        r"(# Copyright \(C\) )(YEAR)( )(THE PACKAGE'S COPYRIGHT HOLDER)"
    )
    R_COPY_REP = r"\g<1>{}\g<3>{}"

    R_EMAIL_SCH = r"(# FIRST AUTHOR )(<EMAIL@ADDRESS>)(, )(YEAR)"
    R_EMAIL_REP = r"\g<1>{}\g<3>{}"

    R_VER_SCH = r"(\"Project-Id-Version: )(.*?)(\\n\")"
    R_VER_REP = r"\g<1>{}\g<3>"

    R_CHAR_SCH = r"(\"Content-Type: text/plain; charset=)(CHARSET)(.*)"
    R_CHAR_REP = r"\g<1>{}\g<3>"

    R_LANG_SCH = r"(\"Language: )(.*?)(\\n\")"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        # header
        str_domain,
        str_version,
        str_author,
        str_email,
        # base prj dir
        dir_prj,
        # in
        list_src,
        dict_clangs,
        # out
        dir_pot,
        dir_po,  # same as dir_linguas
        dir_locale,
        # optional in
        str_tag=None,
        charset=S_ENCODING,
    ):
        """
        Initialize the new object

        Args:
            str_domain: The name of the domain (base name) for output files
                This creates files like "<str_domain>.pot" and
                "<str_domain>.mo", and is used in the .py scripts to bind a
                domain to a locale folder
            str_version: Version info to use in .pot/.po header
            str_author: Author name to use in .pot/.po header
            str_email: Email to use in .pot/.po header

            dir_prj: The main project dir, used for relative paths

            list_src: Where to look for input files
            dict_clangs: The dictionary of file extensions to scan for each
                clang (default: None)
                If ths dict is empty or None, all files will be scanned
                (this is generally considered a "Very Bad Thing").

            dir_pot: Directory to place master .pot file
            dir_po: Directory to place .po files and LINGUAS file
            dir_locale: Directory to place .mo files

            str_tag: Tag that starts a context comment (default: None)
                If this string is empty or None, all comments above an entry
                are included as context.
            charset: the charset to use as the default in the .pot file, and
                any initial .po files created (default: "UTF-8")

        An example format for the dict_clangs arg is:

        {
            "Python": [
                ".py",
            ],
            "Glade": [
                ".ui",
                ".glade",
            ],
            "Desktop": [
                ".desktop"
            ],
        }

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # set header info
        self._str_domain = str_domain
        self._str_version = str_version
        self._str_author = str_author
        self._str_email = str_email

        # set base props
        self._dir_prj = Path(dir_prj)

        # fix up in props
        if list_src is None:
            list_src = []
        self._list_src = list_src
        if dict_clangs is None:
            dict_clangs = {}
        self._dict_clangs = dict_clangs

        # set out props
        self._dir_pot = Path(dir_pot)
        if not self._dir_pot.is_absolute():
            self._dir_pot = self._dir_prj / dir_pot
        self._dir_po = Path(dir_po)
        if not self._dir_po.is_absolute():
            self._dir_po = self._dir_prj / dir_po
        self._dir_locale = Path(dir_locale)
        if not self._dir_locale.is_absolute():
            self._dir_locale = self._dir_prj / dir_locale

        # set optional in props

        # set comment tag
        if str_tag is None:
            str_tag = ""
        self._str_tag = str_tag

        # fix up charset
        if charset is None:
            charset = self.S_ENCODING
        self._charset = charset

        # ----------------------------------------------------------------------

        # fix up list_wlangs
        glob_po = f"**/*{self.S_EXT_PO}"
        self._list_wlangs = list(
            self._dir_po.glob(glob_po, case_sensitive=False)
        )

        # get path to pot file
        self._file_pot = self._dir_pot / f"{self._str_domain}{self.S_EXT_POT}"

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
            cnlib.cnfunctions.CNRunError if anything fails

        Main method of the class, performing its steps. This method can (and
        should) be run, in Mayor Tweed's words, "early and often". You should
        run it every time a source file that contains i18n strings is added,
        edited, or deleted. The ideal scenario is to run it just before the
        repo is synced, so that the .pot file is synced.
        """

        # check for xgettext
        try:
            cp = F.run(self.S_CMD_WHICH_XGT, capture_output=True)
            if cp.stdout == "":
                print(self.S_ERR_NO_XGT)
                return

        # check for error, let someone else handle it
        except F.CNRunError as e:
            raise e

        # ----------------------------------------------------------------------
        # do the steps

        try:
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
    def make_desktop(self, dt_template, dt_out):
        """
        Localize the desktop file using all available wlangs

        Args:
            dt_template: File containing the default information to include in
            the desktop file
                This is the file that pymaker/pybaker modifies using metadata.
            dt_out: Location of the i18n'ed desktop file
                This is the file that will be distributed with your app.

        Raises:
            cnlib.cnfunctions.CNRunError if the make fails

        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final .desktop file.
        """

        # fix params to abs paths
        dt_template = Path(dt_template)
        if not dt_template.is_absolute():
            dt_template = self._dir_prj / dt_template
        dt_out = Path(dt_out)
        if not dt_out.is_absolute():
            dt_out = self._dir_prj / dt_out

        # kill old final desktop to prevent scanning
        if dt_out.exists():
            dt_out.unlink()

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
    # Create a .pot file in the locale folder
    # --------------------------------------------------------------------------
    def _make_pot(self):
        """
        Create a .pot file in the pot folder

        Raises:
            cnlib.cnfunctions.CNRunError if the make fails

        Parses the files for each clang, creating a unified .pot file, which is
        placed in "<dir_pot>/<str_domain>.pot".
        """

        # ok so this is a tricky situation. here are the possible scenarios:
        # 1. create a new, fresh .pot that has never existed before
        # 2. add / edit / remove files to / from a .pot file we have already
        #    created
        # 3. add / edit / remove strings to / from a .pot file we have already
        #    created
        # 4. add / edit / remove clang types to / from a .pot file we have
        #    already created
        # 6. etc., etc., etc
        # how do we do all this (at least in the context of a .pot file)?
        # the simplest answer would seem to be:
        # delete the .pot (if it exists) and start over fresh every time
        # BUT! we need to use the -j (join) flag in order to allow multiple
        # clangs to be combined into one .pot file
        # the solution i have found is:
        # delete the existing .pot file (if it exists)
        # create a new, empty .pot file (if it does not exist, which it
        # shouldn't, race conditions be damned... Python file operations are
        # atomic, right? RIGHT???)
        # run every clang through xgettext, joining it with the previous file
        # until we have a .pot file that contains every string (and only the
        # strings) in dict_clangs
        # step 3: PROFIT! (ha ha ha that joke never gets old...)

        # delete the existing .pot file (if it exists)
        self._file_pot.unlink(missing_ok=True)

        # create a new, empty .pot file if it does not exist
        # NB: this allow us to use the -j flag without error (which would
        # happen if the current file to join does not exist)
        self._file_pot.parent.mkdir(parents=True, exist_ok=True)
        self._file_pot.touch(exist_ok=True)

        # fix up dict_clangs
        self._dict_clangs = self._get_clangs()

        # for each clang name / list of clang files
        for clang_name, clang_files in self._dict_clangs.items():

            if not isinstance(clang_files, list):
                clang_files = list(clang_files)

            # sanity check
            if len(clang_files) == 0:
                continue

            # get initial cmd
            cmd = (
                f"cd {self._dir_prj}; "
                "xgettext "
                # add any comments above string (or msgctxt in ui files)
                # NB: check that all files have appropriate contexts/comments
                # NB: also, no space after -c? weird right?
                f"-c{self._str_tag} "
                # fix some header values (the rest should be fixed in
                # _fix_pot_header)
                # copyright
                # NB: if blank, file is public domain
                # if not included, file is under same license as _str_appname
                # "--copyright-holder "" "
                # version
                # | name | version | Project-Id-Version
                # -----------------------------------
                # |    0 |       0 | PACKAGE VERSION
                # |    0 |       1 | PACKAGE VERSION
                # |    1 |       0 | self._str_domain
                # |    1 |       1 | self._str_domain self._str_version
                f"--package-name {self._str_domain} "
                f"--package-version {self._str_version} "
                # author email
                f"--msgid-bugs-address {self._str_email} "
                # sort entries by file
                "-F "
                # don't add location info (hide path to source)
                # "--no-location "
                # append existing file
                # NB: this is the key to running xgettext multiple times for
                # one domain
                # this allows us to set the -L option for different file types
                # and still end up with one unified .pot file
                "-j "
                # final name of output file
                # NB: note that you can fiddle with the -o, -d, and -p options
                # here, but i find it's just better to use an abs path to the
                # output file
                f"-o {self._file_pot} "
                # add -L for specific exts
                f"-L {clang_name} "
            )

            # add all input files
            paths = [f'"{item}"' for item in clang_files]
            j_paths = " ".join(paths)
            cmd += j_paths

            # do the final command
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

        # fix short desc/copyright/email/version/charset in pot
        self._fix_pot_header(self._file_pot)

        # make rest of folder structure (not necessary but helps new users
        # understand)
        self._dir_locale.mkdir(parents=True, exist_ok=True)
        self._dir_po.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------------
    # Merge any .po files in the pos folder with existing .pot file
    # --------------------------------------------------------------------------
    def _update_pos(self):
        """
        Merge any .po files in the pos folder with existing .pot file

        Raises:
            cnlib.cnfunctions.CNRunError if the make fails

        Whenever a new .pot file is generated using _make_pot, this method will
        produce a new .po file for each wlang that contains the difference
        between the new .pot file and the existing .po file.

        This new .po file should be sent to the translator for each wlang. Then
        when the translator sends back the translated .po file, place it in the
        appropriate dir. Then run pybaker -l to create a new .mo file.
        """

        # get all wlangs to output
        # glob_po = f"**/*{self.S_EXT_PO}"
        # list_pos = list(self._dir_po.glob(glob_po, case_sensitive=False))

        # for each wlang in the po folder
        for po in self._list_wlangs:

            # update existing po file using latest pot
            cmd = self.S_CMD_MERGE_POS.format(po, self._file_pot)
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

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
            if wlang == "":
                print(self.S_ERR_NO_LANG.format(file_po))
                continue

            # get .mo file (output)
            mo_dir = self._dir_locale / str(wlang) / self.S_DIR_LC
            mo_dir.mkdir(parents=True, exist_ok=True)
            mo_file = mo_dir / f"{self._str_domain}{self.S_EXT_MO}"

            # do the command
            cmd = self.S_CMD_MAKE_MOS.format(mo_file, file_po)
            try:
                F.run(cmd, shell=True, capture_output=True)
            except F.CNRunError as e:
                raise e

    # --------------------------------------------------------------------------
    # Scan the source dirs for files with certain extensions
    # --------------------------------------------------------------------------
    def _get_clangs(self):
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

        # ----------------------------------------------------------------------

        # return the result
        return dict_res

    # --------------------------------------------------------------------------
    # Get language code from inside file
    # --------------------------------------------------------------------------
    def _get_wlang_from_file(self, file_po):
        """
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
    # Set the header values for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self, file_pot):
        """
        Set the header values for the pot which will carry over to each po

        Args:
            file_pot: the path object representing the pot file to fix

        Fix the charset in the pot file to a known value so that msgfmt does
        not complain. The charset for an individual file can be set by the
        translator. This is just to keep the compiler from complaining, and
        also aids in testing when no editing is done.
        """

        # open file and get contents
        with open(file_pot, "r", encoding=self.S_ENCODING) as a_file:
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

        # replace author's email
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
        str_rep = self.R_CHAR_REP.format(self._charset)
        text = re.sub(str_pattern, str_rep, text)

        # make all locations relative to project dir
        rep = str(self._dir_prj) + "/"
        text = text.replace(rep, "")

        # save file
        with open(file_pot, "w", encoding=self.S_ENCODING) as a_file:
            a_file.write(text)


# -)

# yes, or no and why
# has a different meaning than
# yes or no, and why
#
# the first one is equivalent to
# yes | (no & why)
# vs
# (yes | no) & why
