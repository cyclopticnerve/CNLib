Module cnlib.cnpot
==================
Run GNU gettext tools to create i18n files for a project

This class converts all marked strings in source files to i18n versions using
xgettext, and creates .pot files in the locale directory. It also uses msgfmt
to convert .po files to .mo files.

The class can handle all xgettext's supported file types by using each language
name as the key for a list of file extensions in a dictionary.

Note that the word "language" here can refer either to the computer language of
the input file (ie. "Python", "Glade") or the written language of the output
file (ie. "English", "Spanish"). I have tried to disambiguate this by using
"clang(s)" to refer to the former, and "wlang(s)" to refer to the latter.

Classes
-------

`CNPotPy(str_domain, str_version, str_author, str_email, dir_prj, list_src, dir_pot, dir_po, dir_locale, str_tag=None, dict_clangs=None, dict_no_ext=None, list_wlangs=None, charset='UTF-8', location=True)`
:   A class to handle making the different I18N files needed for a Python
    project
    
    Methods:
        main: Run the program and make or update the files
        make_desktop: Localize the desktop file using all available wlangs
    
    This class provides methods to create .pot, .po, .mo, and .desktop files
    for internationalizing a Python or PyGObject project.
    
    Initialize the new object
    
    Args:
        str_domain: The name of the domain (base name) for output files
            This creates files like "<str_domain>.pot", "<str_domain>.po",
            and "<str_domain>.mo", and is used in the .py scripts to bind a
            domain to a locale folder
        str_version: Version info to use in .pot/.po header
        str_author: Author name to use in .pot/.po header
        str_email: Email to use in .pot/.po header
    
        dir_prj: The main project dir, used for relative paths
    
        list_src: Where to look for input files
    
        dir_pot: Directory to place master .pot file
        dir_po: Directory to place .po file
        dir_locale: Directory to place .mo files
    
        str_tag: Tag that starts a context comment (default: None)
            If this string is empty or None, all comments above an entry
            are included as context.
        dict_clangs: The dictionary of file extensions to scan for each
        clang (default: None)
            If ths dict is empty or None, all files will be scanned
            (this is generally considered a "Very Bad Thing").
        dict_no_ext: An optional dict mapping files with no extension
        to their clang value (default: None)
        list_wlangs: A list of supported languages to ensure a complete
        file structure in the project dir (default: None)
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
    
    An example format for the dict_no_ext arg is:
    
    {
        "Markdown": [
            "README",
        ],
        "Text": [
            "INSTALL",
            "LICENSE",
        ],
    }
    
    An example format for list_wlangs is:
    [
        "en_US",
        "de_DE.ISO_88591",
        "es",
    ]
    
    Initializes a new instance of the class, setting the default values of
    its properties, and any other code needed to create a new object.

    ### Class variables

    `R_CHAR_REP`
    :

    `R_CHAR_SCH`
    :

    `R_COPY_REP`
    :

    `R_COPY_SCH`
    :

    `R_EMAIL_REP`
    :

    `R_EMAIL_SCH`
    :

    `R_TITLE_REP`
    :

    `R_TITLE_SCH`
    :

    `R_VER_REP`
    :

    `R_VER_SCH`
    :

    `S_CHARSET`
    :

    `S_CMD_DSK`
    :

    `S_CMD_MAKE_MOS`
    :

    `S_CMD_MERGE_POS`
    :

    `S_DIR_LC`
    :

    `S_ERR_NOT_ABS`
    :

    `S_ERR_NOT_DIR`
    :

    `S_EXT_MO`
    :

    `S_EXT_PO`
    :

    `S_EXT_POT`
    :

    `S_FILE_LINGUAS`
    :

    ### Methods

    `main(self)`
    :   Run the program and make or update the files
        
        Main method of the class, performing its steps. This method can (and
        should) be run, in Mayor Tweed's words, "early and often". You should
        run it every time a source file that contains i18n strings is added,
        edited, or deleted. The ideal scenario is to run it just before the
        repo is synced, so that the .pot file is synced.

    `make_desktop(self, dt_template, dt_out)`
    :   Localize the desktop file using all available wlangs
        
        Args:
            dt_template: File containing the default information to include in
            the desktop file
                This is the file that pymaker/pybaker modifies using metadata.
            dt_out: Location of the i18n'ed desktop file
                This is the file that will be distributed with your app.
        
        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final .desktop file.