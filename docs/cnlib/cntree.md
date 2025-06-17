Module cnlib.cntree
===================
This module creates a tree of the specified directory, with paths being
ignored by the filter list and names being formatted according to the
specified formats.

Classes
-------

`CNTree(start_dir, filter_list=None, fmt_name='', dir_format='', file_format='', dirs_only=False, ignore_case=True)`
:   Generate a file tree in text format with the names formatted according to
    some format strings
    
    Methods:
        main: Creates a tree from the given start directory, using filter list,
        directory and file formats
    
    This class builds the tree as a complete string, ready to be printed to
    stdout or a file.
    
    Initializes the new object
    
    Args:
        start_dir: String or Path to the root directory of the tree
        filter_list: List of directory/file names to filter out (default:
        None)
        dir_format: Format to use for directories (default:"$NAME/")
        file_format: Format to use for files (default: "$NAME")
        dirs_only: Only list directories (default: False)
        ignore_case: Sort entries regardless of case. If False,
        uppercase alpha characters take precedence.
    
    Creates a tree from the given start directory.
    
    The start_dir can be an absolute path, a relative path, or a Path
    object, but MUST point to a directory.
    
    If start_dir does not point to a directory, an OSError will be raised.
    
    If start_dir == None, an OSError will be raised.
    
    If start_dir == "", the current directory is used.
    
    Items in the filter list will be skipped. These items can be absolute or
    relative directory or file paths, or a glob.
    
    Example:
    
        filter_list = ["Foo/bar.txt", "Foo"]
    
    An entry of "Foo/bar.txt" will skip a file with the absolute path
    "\<start dir\>/Foo/bar.txt".
    
    An entry of "Foo" (if it points to a directory) will skip a
    directory with the absolute path "\<start dir\>/Foo/" and
    everything under it.
    
    Globs are also acceptable, see
    https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
    
    The format strings for directory and file names will have the value
    of "FORMAT_NAME" replaced by the directory or file name.
    
    Example: (assuming FORMAT_NAME is set to "$NAME")
    
        dir_format = " [] $NAME/"
        item.name = "Foo"
        result = " [] Foo/"
    
    Also, leading spaces in dir_format, when applied to the start_dir
    name, will be left-trimmed to make the tree start at the first
    column.
    
    Initializes a new instance of the class, setting the default values
    of its properties, and any other code that needs to run to create a
    new object.

    ### Class variables

    `S_CHAR_ELL`
    :

    `S_CHAR_HORZ`
    :

    `S_CHAR_SPACE`
    :

    `S_CHAR_TEE`
    :

    `S_CHAR_VERT`
    :

    `S_CONNECTOR_ELL`
    :

    `S_CONNECTOR_TEE`
    :

    `S_ERR_NOT_ABS`
    :

    `S_ERR_NOT_DIR`
    :

    `S_FORMAT_DIR`
    :

    `S_FORMAT_FILE`
    :

    `S_FORMAT_NAME`
    :

    `S_PREFIX_NONE`
    :

    `S_PREFIX_VERT`
    :

    `S_SORT_ORDER`
    :

    ### Methods

    `main(self)`
    :   Creates a tree from the given start directory, using filter list,
        directory and file formats
        
        Returns:
            The current tree as a string
        
        Raises:
            OSError: If the start_dir parameter is None or does not contain
                a path to a valid directory