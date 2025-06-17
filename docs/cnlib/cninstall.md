Module cnlib.cninstall
======================
The class to use for installing/uninstalling

Classes
-------

`CNInstall()`
:   The class to use for installing/uninstalling
    
    Methods:
        make_install_cfg: Make a valid install config file
        make_uninstall_cfg: Make a valid uninstall config file
        fix_desktop_file: Fix .desktop file, for paths and such
        install: Install the program
        uninstall: Uninstall the program
    
    This class provides functions to create install/uninstall config files, and
    performs the install and uninstall operations.
    
    Initialize the class
    
    Creates a new instance of the object and initializes its properties.

    ### Class variables

    `R_ICON_REP`
    :

    `R_ICON_SCH`
    :

    `R_VERSION`
    :

    `R_VERSION_GROUP_MAJ`
    :

    `R_VERSION_GROUP_MIN`
    :

    `R_VERSION_GROUP_REV`
    :

    `S_ASK_CONFIRM`
    :

    `S_ASK_VER_OLDER`
    :

    `S_ASK_VER_SAME`
    :

    `S_CMD_CREATE`
    :

    `S_CMD_INSTALL`
    :

    `S_CMD_INST_LIB`
    :

    `S_CMD_VENV_ACTIVATE`
    :

    `S_DRY_ACTION`
    :

    `S_DRY_DESK_ICON`
    :

    `S_DRY_DEST`
    :

    `S_DRY_HELP`
    :

    `S_DRY_OPTION`
    :

    `S_ERR_DST_PATH`
    :

    `S_ERR_NOT_FOUND`
    :

    `S_ERR_NOT_JSON`
    :

    `S_ERR_NO_SUDO`
    :

    `S_ERR_SRC_PATH`
    :

    `S_ERR_VERSION`
    :

    `S_KEY_DICT_INSTALL`
    :

    `S_KEY_LIST_UNINST`
    :

    `S_KEY_NAME`
    :

    `S_KEY_VERSION`
    :

    `S_MSG_COPY_START`
    :

    `S_MSG_DEL_START`
    :

    `S_MSG_DONE`
    :

    `S_MSG_DSK_START`
    :

    `S_MSG_FAIL`
    :

    `S_MSG_INST_END`
    :

    `S_MSG_INST_START`
    :

    `S_MSG_LIBS_START`
    :

    `S_MSG_REQS_START`
    :

    `S_MSG_UNINST_END`
    :

    `S_MSG_UNINST_START`
    :

    `S_MSG_VENV_START`
    :

    `S_MSG_VER_ABORT`
    :

    ### Methods

    `fix_desktop_file(self, desk_file, path_icon, dry=False)`
    :   Fix .desktop file, for paths and such
        
        Args:
            desk_file: The path to the desktop file to be modified
            path_icon: The path to the program's icon, relative to user home
            dry: If True, do not copy files, ony print the action (default:
            False)
        
        Fixes entries in the .desktop file (absolute paths, etc.)
        Currently only fixes absolute path to icon.

    `install(self, dir_assets, path_lib, path_cfg_inst, path_cfg_uninst, dir_usr_inst, dir_venv, path_reqs, dry=False)`
    :   Install the program
        
        Args:
            dir_assets: Path to the assets folder where all of the program
            files are put in dist. This is the base source path to use when
            copying files to the user's computer
            path_lib: Path to the dist's lib folder, ie. "assets/lib"
            path_cfg_inst: Path to the file that contains the current install
            dict info
            path_cfg_uninst: Path to the currently installed program's
            uninstall dict info
            dir_usr_inst: The program's install folder in which to make a venv
            dir_venv: The path to the venv folder to create
            path_reqs: Path to the requirements.txt file to add requirements to
            the venv
            dry: If True, do not copy files, ony print the action (default:
            False)
        
        Runs the install operation.

    `make_install_cfg(self, name, version, dict_install)`
    :   Make a valid install config file
        
        Args:
            name: Program name
            version: New version number to compare to any installed version
            dict_install: Dict of assets to install
        
        Returns:
            A properly formatted install config dict to save to a file
        
        This method creates a config file for use by install.py. The dict
        format can be found below.

    `make_uninstall_cfg(self, name, version, list_uninst)`
    :   Make a valid uninstall config file
        
        Args:
            name: Program name
            version: Initial program version from pyplate.py
            list_uninstall: List of assets to uninstall
        
        Returns:
            A properly formatted uninstall config dict to save to a file
        
        This method creates a config file for use by uninstall.py. The dict
        format can be found below.

    `uninstall(self, path_cfg, dry=False)`
    :   Uninstall the program
        
        Args:
            path_cfg: Path to the file that contains the uninstall dict info
            dry: If True, do not remove files, ony print the action (default:
            False)
        
        Runs the uninstall operation.