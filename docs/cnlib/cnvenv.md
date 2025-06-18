Module CNLib.cnlib.cnvenv
=========================
A class to make handling of venv folders easier

Classes
-------

`CNVenv(dir_prj, dir_venv)`
:   A class to make handling of venv folders easier
    
    Methods:
        create: Creates a new venv given the __init__ params
        install_reqs: Install packages to venv from the reqs_file property
        freeze: Freeze packages in the venv folder to the file_reqs property
    
    This class provides methods to create, freeze, and install dependencies
    in the project's venv folder.
    
    Initialize the new object
    
    Args:
        dir_prj: The path to the project's root dir (can be a string or a
        Path object)
        dir_venv: The path or name of the resulting venv folder (can be a
        string or a Path object, absolute or relative to dir_prj)
    
    Initializes a new instance of the class, setting the default values of
    its properties, and any other code needed to create a new object.

    ### Class variables

    `S_CMD_CREATE`
    :

    `S_CMD_FREEZE`
    :

    `S_CMD_INSTALL`
    :

    `S_ERR_NOT_ABS`
    :

    `S_ERR_NOT_DIR`
    :

    ### Methods

    `create(self)`
    :   Creates a new venv given the __init__ params
        
        Creates a new venv folder with the parameters provided at create time.

    `freeze(self, file_reqs)`
    :   Freeze packages in the venv folder to the file_reqs property
        
        Args:
            file_reqs: File to save requirements
        
        Freezes current packages in the venv dir into a file for easy
        installation.

    `install_reqs(self, file_reqs)`
    :   Install packages to venv from the reqs_file property
        
        Args:
            file_reqs: File to load requirements
        
        This method takes requirements in the reqs_file property and installs
        them in the dir_venv property.