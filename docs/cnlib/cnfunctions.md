Module cnlib.cnfunctions
========================
A collection of common functions used by CN software

Functions:
    pascal_case: Convert a class name to it's Pascal equivalent
    do_bool: Convert other values, like integers or strings, to bools
    dpretty: Pretty print a dict
    lpretty: Pretty print a list
    pp: Pretty print a dictionary or list
    combine_dicts: Update a dictionary with one or more dictionaries
    sh: Run a command string in the shell
    load_dicts: Combines dictionaries from all found paths
    save_dict: Save a dictionary to all paths

Functions
---------

`combine_dicts(dicts_new, dict_old=None)`
:   Update a dictionary with entries from another dict
    
    Args:
        dicts_new: A dictionary or list of dictionaries containing new
        keys/values to be updated in the old dictionary
        dict_old: The dictionary defined as the one to receive updates
    
    Returns:
        The updated dict_old, filled with updates from dict_new
    
    This function takes key/value pairs from each of the new dicts and
    adds/overwrites these keys and values in dict_old, preserving any values
    that are blank or None in dict_new. It is also recursive, so a dict or list
    as a value will be handled correctly.

`do_bool(val)`
:   Convert other values, like integers or strings, to bools
    
    Args:
        val: The value to convert to a bool
    
    Returns:
        A boolean value converted from the argument
    
    Converts integers and strings to boolean values based on the rules.

`dpretty(dict_print, indent_size=4, indent_level=0, label=None)`
:   Pretty print a dict
    
    Args:
        dict_print: The dictionary to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        indent_level: The number of indent levels to use for this part of the
        print process (default: 0)
        label: The string to use as a label (default: None)
    
    Returns:
        The formatted string to print
    
    Raises:
        OSError if the first param is not a dict
    
    Formats a dictionary nicely so it can be printed to the console.

`load_dicts(paths, start_dict=None)`
:   Combines dictionaries from all found paths
    
    Args:
        paths: The file path or list of file paths to load
        start_dict: The starting dict and final dict after combining (default:
        None)
    
    Returns:
        The final combined dictionary
    
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not a valid JSON file
    
    Load the dictionaries from all files and use combine_dicts to combine them.

`lpretty(list_print, indent_size=4, indent_level=0, label=None)`
:   Pretty print a list
    
    Args:
        list_print: The list to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        indent_level: The number of indent levels to use for this part of the
        print process (default: 0)
        label: The string to use as a label (default: None)
    
    Returns:
        The formatted string to print
    
    Raises:
        OSError if the first param is not a list
    
    Formats a list nicely so it can be printed to the console.

`pascal_case(a_str)`
:   Format a string in Pascal case
    
    Args:
        a_str: A string to convert to Pascal case
    
    Returns;
        The Pascal cased string
    
    Formats the given string to a Pascal case equivalent, ie. "my_class"
    becomes "MyClass".

`pp(obj, indent_size=4, label=None)`
:   Pretty print a dictionary or list
    
    Args:
        obj: The dictionary or list to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        label: The string to use as a label (default: None)
    
    Returns:
        The object formatted for printing
    
    Raises:
        OSError if the first param is not a dict or list
    
    Formats a dictionary or list nicely and prints it to the console. Note that
    this method includes magic commas in the output, and therefore cannot be
    used to create true JSON-compatible strings. It should only be used for
    debugging.

`save_dict(a_dict, paths)`
:   Save a dictionary to all paths
    
    Args:
        a_dict: The dictionary to save to the file
        paths: The path or list of paths to save to
    
    Raises:
        OSError: If the file does not exist and can't be created
    
    Save the dictionary to a file at all the specified locations.

`sh(cmd, shell=False)`
:   Run a program or command string in the shell
    
    Args:
        cmd: The command line to run
        shell: If False (the default), run the cmd as one long string. If True,
        split the cmd into separate arguments
    
    Returns:
        The result of running the command line, as a
        subprocess.CompletedProcess object
    
    This is just a dumb convenience method to use subprocess with a string
    instead of having to convert a string to an array with shlex every time I
    need to run a shell command.