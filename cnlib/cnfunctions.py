# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnfunctions.py                                        |     ()     |
# Date    : 02/21/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines

"""
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
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import json
from pathlib import Path
import re
import shlex
import subprocess

# ------------------------------------------------------------------------------
# Constant strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# bools

B_DEBUG = False

# ------------------------------------------------------------------------------
# strings

S_ERR_NOT_DICT = "dpretty object is not a dict"
S_ERR_NOT_LIST = "lpretty object is not a list"
S_ERR_NOT_DICT_OR_LIST = "pp object is not a dict or list"
S_ERR_SHELL = "shell process failed"
# NB: format param is dict file path
S_ERR_NOT_EXIST = "dict file '{}' does not exist"
# NB: format param is dict file path
S_ERR_NOT_VALID = "dict file '{}' is not a valid JSON file"
# NB: format param is dict file path
S_ERR_NOT_CREATE = "dict file '{}' could not be created"
S_ERR_VERSION = "One or both version numbers are invalid"
# NB: format param is file path
S_ERR_NOT_FOUND = "File {} not found"
# NB: format param is file path
S_ERR_NOT_JSON = "File {} is not a JSON file"

# questions
S_ASK_YES = "y"
S_ASK_NO = "n"

# encoding
S_ENCODING = "UTF-8"

# ------------------------------------------------------------------------------
# ints

# version check results
I_VER_OLDER = -1
I_VER_SAME = 0
I_VER_NEWER = 1
I_VER_ERROR = -2

# ------------------------------------------------------------------------------
# colors

C_FG_NONE = 0
C_FG_BLACK = 30
C_FG_RED = 31
C_FG_GREEN = 32
C_FG_YELLOW = 33
C_FG_BLUE = 34
C_FG_MAGENTA = 35
C_FG_CYAN = 36
C_FG_WHITE = 37

C_BG_NONE = 0
C_BG_BLACK = 40
C_BG_RED = 41
C_BG_GREEN = 42
C_BG_YELLOW = 43
C_BG_BLUE = 44
C_BG_MAGENTA = 45
C_BG_CYAN = 46
C_BG_WHITE = 47

# ------------------------------------------------------------------------------
# regexes

# regex to compare version numbers
R_VERSION_VALID = (
    r"^"
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-("
    r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*"
    r"))?"
    r"(?:\+("
    r"[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*"
    r"))?"
    r"$"
)
R_VERSION_GROUP_MAJ = 1
R_VERSION_GROUP_MIN = 2
R_VERSION_GROUP_REV = 3
R_VERSION_GROUP_PRE = 4
R_VERSION_GROUP_META = 5

# ------------------------------------------------------------------------------
# lists

# if it is in this list, it is True, else false
# NB: strings here should be all lowercase
L_RULES_TRUE = [
    "true",
    "1",
    "yes",
    "y",
]

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to encapsulate subprocess.run() exceptions
# ------------------------------------------------------------------------------
class CNRunError(Exception):
    """
    A class to encapsulate run exceptions
    """

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self, cmd, returncode, stdout, stderr, output):
        """
        Docstring for __init__

        :param self: Description
        :param cmd: Description
        :param returncode: Description
        :param stdout: Description
        :param stderr: Description
        :param output: Description
        """

        # call super __init__
        super().__init__()

        # set properties from params
        self.cmd = cmd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.output = output

    # --------------------------------------------------------------------------
    # Return a string representation of an instance of the class
    # --------------------------------------------------------------------------
    def __str__(self):
        return (
            f"cmd: {self.cmd}, "
            f"returncode: {self.returncode}, "
            f"stdout: {self.stdout}, "
            f"stderr: {self.stderr}, "
            f"output: {self.output}"
        )


# ------------------------------------------------------------------------------
# Public methods
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Format a string in Pascal case
# ------------------------------------------------------------------------------
def pascal_case(a_str):
    """
    Format a string in Pascal case

    Args:
        a_str: A string to convert to Pascal case

    Returns;
        The Pascal cased string

    Formats the given string to a Pascal case equivalent, ie. "my_class"
    becomes "MyClass".
    """

    # do formatting
    name_pascal = a_str
    name_pascal = name_pascal.replace("_", " ")
    name_pascal = name_pascal.replace("-", " ")
    name_pascal = name_pascal.title()
    name_pascal = name_pascal.replace(" ", "")

    # return result
    return name_pascal


# ------------------------------------------------------------------------------
# Convert other values, like integers or strings, to bools
# ------------------------------------------------------------------------------
def do_bool(val):
    """
    Convert other values, like integers or strings, to bools

    Args:
        val: The value to convert to a bool

    Returns:
        A boolean value converted from the argument

    Converts integers and strings to boolean values based on the rules.
    """

    # lower all test vals
    rules_true = [item.lower() for item in L_RULES_TRUE]

    # return result
    return str(val).lower() in rules_true


# ------------------------------------------------------------------------------
# Pretty print a dict
# ------------------------------------------------------------------------------
def dpretty(dict_print, indent_size=4, indent_level=0, label=None):
    """
    Pretty print a dict

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
    """

    # sanity check
    if not isinstance(dict_print, dict):
        raise OSError(S_ERR_NOT_DICT)

    # default out
    out = ""

    # print label
    if label is not None:
        out += label + ": "

    # convert indent_size to string and multiply by indent_level
    indent_str = (" " * indent_size) * (indent_level)

    # items will need an extra indent, since they don't recurse
    indent_str_next = (" " * indent_size) * (indent_level + 1)

    # default result opening brace (no indent in case it is nested and is
    # preceded by a key)
    out += indent_str + "{\n"

    # for each entry
    for k, v in dict_print.items():

        # print the key
        out += indent_str_next + f'"{k}": '

        # if the value is a list
        if isinstance(v, list):

            # recurse the value and increase indent level
            ret = (
                lpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            ret = ret.lstrip()
            out += ret

        # if the value is a dict
        elif isinstance(v, dict):

            # recurse the value and increase indent level
            ret = (
                dpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            ret = ret.lstrip()
            out += ret

        # if it is a single entry (str, int, bool)
        else:

            # print the value, quoting it if it is a string
            if isinstance(v, str):
                out += f'"{v}",\n'
            else:
                out += f"{v},\n"

    # get original indent
    indent_str = (" " * indent_size) * indent_level

    # # add closing bracket
    out += indent_str + "}"

    # return result
    return out


# ------------------------------------------------------------------------------
# Pretty print a list
# ------------------------------------------------------------------------------
def lpretty(list_print, indent_size=4, indent_level=0, label=None):
    """
    Pretty print a list

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
    """

    # sanity check
    if not isinstance(list_print, list):
        raise OSError(S_ERR_NOT_LIST)

    # default out
    out = ""

    # print label
    if label is not None:
        out += label + ": "

    # convert indent_size to string and multiply by indent_level
    indent_str = (" " * indent_size) * (indent_level)

    # items will need an extra indent, since they don't recurse
    indent_str_next = (" " * indent_size) * (indent_level + 1)

    # default result opening brace (no indent in case it is nested and is
    # preceded by a key)
    out += indent_str + "[\n"

    # for each entry
    for v in list_print:

        # if the value is a list
        if isinstance(v, list):

            # recurse the value and increase indent level
            ret = (
                lpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            out += ret

        # if the value is a dict
        elif isinstance(v, dict):

            # recurse the value and increase indent level
            ret = (
                dpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            out += ret

        # if it is a single entry (str, int, bool)
        else:

            # print the value, quoting it if it is a string
            if isinstance(v, str):
                out += indent_str_next + f'"{v}",\n'
            else:
                out += indent_str_next + f"{v},\n"

    # get original indent
    indent_str = (" " * indent_size) * indent_level

    # # add closing bracket
    out += indent_str + "]"

    # return result
    return out


# ------------------------------------------------------------------------------
# Pretty print a list or dictionary
# ------------------------------------------------------------------------------
def pp(obj, indent_size=4, label=None):
    """
    Pretty print a dictionary or list

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
    """

    # the default result
    result = ""

    # call different pretty functions depending on the object type
    if isinstance(obj, dict):
        result = dpretty(obj, indent_size, 0, label)
    elif isinstance(obj, list):
        result = lpretty(obj, indent_size, 0, label)
    else:
        raise OSError(S_ERR_NOT_DICT_OR_LIST)

    # print the result
    print(result)


# ------------------------------------------------------------------------------
# Update a dictionary with entries from another dict
# ------------------------------------------------------------------------------
def combine_dicts(dicts_new, dict_old=None):
    """
    Update a dictionary with entries from another dict

    Args:
        dicts_new: A dictionary or list of dictionaries containing new
        keys/values to be updated in the old dictionary
        dict_old: The dictionary defined as the one to receive updates
        (default: None)

    Returns:
        The updated dict_old, filled with updates from dict_new

    This function takes key/value pairs from each of the new dicts and
    adds/overwrites these keys and values in dict_old, preserving any values
    that are blank or None in dict_new. It is also recursive, so a dict or list
    as a value will be handled correctly.
    *NOTE: This function DOES NOT test for type mismatches in values for
    matching keys!!!
    So if a new dict has a key of "A" and a value of type "str", and the old
    dict has a key of "A" with a value of type "int", bad things will
    happen!!!
    """

    # default return val
    if dict_old is None:
        dict_old = {}
    else:
        dict_old = dict(dict_old)

    # sanity checks
    if not isinstance(dicts_new, list):
        dicts_new = [dicts_new]
    if len(dicts_new) == 0:
        return dict_old

    # go through the new dicts in order
    for dict_new in dicts_new:

        # for each k,v pair in dict_new
        for k, v in dict_new.items():

            # if the value is a dict
            if isinstance(v, dict):
                # recurse using the current key and value
                dict_old[k] = combine_dicts(v, dict_old.get(k, None))
                # dict_old[k] = combine_dicts(v, dict_old[k])
                continue

            # if the value is not a dict or a list
            # just copy value from one dict to the other
            dict_old[k] = v

    # return the updated dict_old
    return dict_old


# ------------------------------------------------------------------------------
# Run a program or shell command string
# ------------------------------------------------------------------------------
def run(cmd, shell=False):
    """
    Run a program or shell command string

    Args:
        cmd: The command to run
        shell: If False (the default), run the cmd as one long string. If True,
        split the cmd into separate arguments

    Returns:
        The result of running the command line, as a
        subprocess.CompletedProcess object

    Raises:
        CNRunError if the command is invalid or the process fails

    This is just a dumb convenience method to use subprocess with a string
    instead of having to convert a string to an array with shlex every time. It
    also combines FileNotFoundError and CalledProcessError into one CNRunError.
    """

    # sanity check to make sure cmd is a string
    cmd = str(cmd)

    # if not shell, split into bin/cli options
    # NB: if shell, we only want the stuff after ["sh", "-c"], which is what
    # would be typed at the command prompt (i.e. all one long command string)
    if not shell:
        cmd = shlex.split(cmd)

    # get result of running the shell command or bubble up an error
    try:
        cp = subprocess.run(
            # the cmd or array of commands
            cmd,
            # if check is True, an exception will be raised if the return code
            # is not 0
            # if check is False, no exception is raised but cp will be None,
            # meaning you have to test for it in the calling function
            # but that also means you have no information on WHY it failed
            # because stderr comes from the CalledProcessError IF
            # capture_output=True
            check=True,
            # put stdout/stderr into cp/cpe
            capture_output=True,
            # convert stdout/stderr from bytes to text
            encoding=S_ENCODING,
            text=True,
            # whether the call is a file w/ params (False) or a direct shell
            # input (True)
            shell=shell,
        )

        # return the result
        return cp

    # the first item in the list is not a bin
    # NB: try these:
    # cmd = "cd /", shell = False: fail
    # cmd = "cd /", shell = True: pass
    # cmd = "ls -l", shell = False: pass
    # cmd = "ls -l", shell = True: pass

    # check if first item is bin, if shell false
    except FileNotFoundError as fnfe:
        # NB: fnfe already has a nice __str__, so use that in the stderr
        # also output = stdout, which is kinda pointless for this error
        # NB: print(exc) gives ALL properties
        # print(exc.stderr) give concise output
        exc = CNRunError(
            cmd, fnfe.errno, fnfe.filename, f"{fnfe}", fnfe.filename
        )
        raise exc from fnfe

    # cmd ran but failed
    except subprocess.CalledProcessError as cpe:
        # NB: here we use the regular stderr as concise output
        exc = CNRunError(
            cpe.cmd, cpe.returncode, cpe.stdout, cpe.stderr, cpe.output
        )
        raise exc from cpe


# ------------------------------------------------------------------------------
# Combines dictionaries from all found paths
# ------------------------------------------------------------------------------
def load_dicts(paths, start_dict=None):
    """
    Combines dictionaries from all found paths

    Args:
        paths: The file path or list of file paths to load start_dict: The
        starting dict and final dict after combining (default: None)

    Returns:
        The final combined dictionary

    Raises:
        OSError: If the file does not exist or the file is not a valid JSON
        file

    Load the dictionaries from all files and use combine_dicts to combine them.
    """

    # sanity check
    if not isinstance(paths, list):
        paths = [paths]

    # set the default result
    if start_dict is None:
        start_dict = {}

    # loop through possible files
    for path in paths:

        # sanity checks
        if not path:
            continue
        path = Path(path).resolve()

        # try each option
        try:

            # open the file
            with open(path, "r", encoding=S_ENCODING) as a_file:
                # load dict from file
                new_dict = json.load(a_file)

                # combine new dict with previous
                start_dict = combine_dicts(new_dict, start_dict)

        # file not found
        except FileNotFoundError as e:
            raise OSError(S_ERR_NOT_FOUND.format(path)) from e

        # not valid json in file
        except json.JSONDecodeError as e:
            raise OSError(S_ERR_NOT_JSON.format(path)) from e

    # return the final dict
    return start_dict


# ------------------------------------------------------------------------------
# Save a dictionary to all paths
# ------------------------------------------------------------------------------
def save_dict(a_dict, paths):
    """
    Save a dictionary to all paths

    Args:
        a_dict: The dictionary to save to the file
        paths: The path or list of paths to save to

    Raises:
        OSError: If the file does not exist and can't be created

    Save the dictionary to a file at all the specified locations.
    """

    # sanity checks
    if not isinstance(paths, list):
        paths = [paths]
    if len(paths) == 0:
        return

    # loop through possible files
    for path in paths:

        # sanity checks
        if not path:
            continue
        path = Path(path).resolve()

        # try each path
        try:

            # first make dirs
            path.parent.mkdir(parents=True, exist_ok=True)

            # open the file
            with open(path, "w", encoding=S_ENCODING) as a_file:
                # save dict tp file
                json.dump(a_dict, a_file, indent=4)

        # raise an OS Error
        except OSError as e:
            raise OSError(S_ERR_NOT_CREATE.format(path)) from e


# ------------------------------------------------------------------------------
# Create a dialog-like question and return the result
# ------------------------------------------------------------------------------
def dialog(
    message, buttons, default="", loop=False, btn_sep="/", msg_fmt="{} [{}]: "
):
    """
    Create a dialog-like question and return the result

    Args:
        message: The message to display
        buttons: List of single char answers to the question
        default: The button item to return when the user presses Enter at the
            question (default: "")
        loop: If True and the user enters an invalid response, keep asking the
        question. If False, return an empty string for an invalid response
        (default: False)
        btn_sep: Char to use to separate button items
        msg_fmt: Format string to present message/buttons to the user

    Returns:
        A lowercased string that matches a button, or an empty string under
        certain conditions

    This method returns the string entered on the command line in response to a
    question. If the entered option does not match any of the buttons, the
    question is asked again. If you set a default and the option entered is
    just the Return key, the default string will be returned. If no default is
    present, the entered string must match one of the buttons array values. All
    returned values are lowercased. The question will be repeatedly printed to
    the screen until a valid entry is made.

    Note that if default == "", pressing Enter is not considered a valid entry.
    So if the default is empty and loop is True, the user MUST enter a valid
    response or the dialog will loop forever.
    """

    # --------------------------------------------------------------------------

    # add buttons to message
    btns_all = btn_sep.join(buttons)
    str_fmt = msg_fmt.format(message, btns_all)

    # --------------------------------------------------------------------------

    # assume loop == True
    while True:

        # ask the question, get the result (first char only/empty)
        inp = input(str_fmt)
        if len(inp) > 0:
            inp = inp[0]

        # ----------------------------------------------------------------------
        # button correct, done
        if inp in buttons:
            return inp

        # ----------------------------------------------------------------------
        # wrong answer

        # default set
        if default != "":

            if inp == "":
                return default

        # no loop, return blank
        if not loop:
            return ""


# ------------------------------------------------------------------------------
# Compare two semantic versions
# ------------------------------------------------------------------------------
def comp_sem_ver(ver_old, ver_new):
    """
    Compare two semantic versions

    Args:
        ver_old: The old version to compare
        ver_new: The new version to compare

    Returns:
        An integer showing the relationship between the two version

    Compare two semantic versions.
    """

    # sanity checks
    if not ver_old or ver_old == "":
        return I_VER_ERROR
    if not ver_new or ver_new == "":
        return I_VER_ERROR
    if ver_old == ver_new:
        return I_VER_SAME

    # --------------------------------------------------------------------------

    # compare version string parts (only x.x.x)
    res_old = re.search(R_VERSION_VALID, ver_old)
    res_new = re.search(R_VERSION_VALID, ver_new)

    # if either version string is None
    if not res_old or not res_new:
        return I_VER_ERROR

    # make a list of groups to check
    lst_groups = [
        R_VERSION_GROUP_MAJ,
        R_VERSION_GROUP_MIN,
        R_VERSION_GROUP_REV,
    ]

    # for each part as int
    for group in lst_groups:
        old_val = int(res_old.group(group))
        new_val = int(res_new.group(group))

        # slide out at the first difference
        if old_val < new_val:
            return I_VER_NEWER
        if old_val > new_val:
            return I_VER_OLDER

    # --------------------------------------------------------------------------

    # still going, check pre
    pre_old = res_old.group(R_VERSION_GROUP_PRE)
    pre_new = res_new.group(R_VERSION_GROUP_PRE)

    # simple pre rule compare
    if not pre_old and pre_new:
        return I_VER_OLDER
    if pre_old and not pre_new:
        return I_VER_NEWER
    if not pre_old and not pre_new:
        return I_VER_SAME

    # --------------------------------------------------------------------------

    # if pre_old and pre_new:

    # split pre on dots
    lst_pre_old = pre_old.split(".")
    lst_pre_new = pre_new.split(".")

    # get number of parts
    len_pre_old = len(lst_pre_old)
    len_pre_new = len(lst_pre_new)

    # get shorter of two
    shortest = len_pre_old if len_pre_old <= len_pre_new else len_pre_new

    # for each part in shortest
    for index in range(shortest):

        # get each value at position
        old_val = lst_pre_old[index]
        new_val = lst_pre_new[index]

        # 1. both numbers
        if old_val.isdigit() and new_val.isdigit():
            tmp_old_val = int(old_val)
            tmp_new_val = int(new_val)

            # slide out at the first difference
            if tmp_old_val > tmp_new_val:
                return I_VER_OLDER
            if tmp_old_val < tmp_new_val:
                return I_VER_NEWER

        # 2. both alphanumeric
        if not old_val.isdigit() and not new_val.isdigit():
            lst_alpha = [old_val, new_val]
            lst_alpha.sort()

            idx_old = lst_alpha.index(old_val)
            idx_new = lst_alpha.index(new_val)

            if idx_old > idx_new:
                return I_VER_OLDER
            if idx_old < idx_new:
                return I_VER_NEWER

        # 3 num vs alphanumeric
        if old_val.isdigit() and not new_val.isdigit():
            return I_VER_OLDER
        if not old_val.isdigit() and new_val.isdigit():
            return I_VER_NEWER

        # 4 len
        if len_pre_old > len_pre_new:
            return I_VER_OLDER
        if len_pre_new > len_pre_old:
            return I_VER_NEWER

    # --------------------------------------------------------------------------

    # error in one or both versions
    return I_VER_SAME


# ------------------------------------------------------------------------------
# Print a string in color
# ------------------------------------------------------------------------------
def printc(
    *values, sep=" ", end="\n", file=None, flush=False, fg=0, bg=0, bold=False
):
    """
    Print a string in color

    Args:
        *values: A variable number of string arguments
        sep: The string used to join *values (default: ' ')
        end: The character(s) to print after the *values (default:'\\n')
        file: The file object to print to or, if None, print to stdout \
        (default: None)
        flush: Whether to force the output buffer to write immediately, \
            rather than waiting for it to fill
        fg: The foreground color of the text as a C_FG_XXX value (see below). \
        If 0, use default terminal color (default: 0)
        bg: The background color of the text as a C_FG_XXX value (see below). \
        If 0, use default terminal color (default: 0)
        bold: Whether the text is bold (duh) (default:False)

    This function prints something to the console, just like print(), but with
    COLOR! and BOLD!\n
    The first five parameters are EXACTLY the same as print()
    and the last three are as follows:\n
    \n
    fg: The foreground color of the text to print. This can be one of the
    following values:\n
    \n
    C_FG_NONE (use the terminal default)\n
    C_FG_BLACK\n
    C_FG_RED\n
    C_FG_GREEN\n
    C_FG_YELLOW\n
    C_FG_BLUE\n
    C_FG_MAGENTA\n
    C_FG_CYAN\n
    C_FG_WHITE\n
    \n
    bg: The background (or highlight) color of the text to print. This can
    be one of the following values:\n
    \n
    C_BG_NONE (use the terminal default)\n
    C_BG_BLACK\n
    C_BG_RED\n
    C_BG_GREEN\n
    C_BG_YELLOW\n
    C_BG_BLUE\n
    C_BG_MAGENTA\n
    C_BG_CYAN\n
    C_BG_WHITE\n
    \n
    A note about the background color:\n
    Setting the background color will (almost?) always set the foreground color
    to white. So no cyan text on a magenta background.
    """

    # NB: every option has a unique value and order does not matter
    # the default array of text options
    arr_opt = []

    # maybe set fg
    if fg != 0:
        arr_opt.append(str(fg))

    # maybe set bg
    if bg != 0:
        arr_opt.append(str(bg))

    # maybe set bold
    if bold:
        arr_opt.append("1")

    # put arr_opt together
    color_val = ";".join(arr_opt)  # '32;42;1', '42'

    # get open sequence
    color_start = f"\033[{color_val}m"

    # get the close sequence (reset fg/bg/bold)
    color_end = "\033[0m"

    # ------------------------------------------------------------------------------

    # get the full string
    value = sep.join(values)

    # split into lines
    lines = value.split("\n")

    # a list of newline-separated strings in the final string
    wrapped_lines = []

    # for each string
    for line in lines:
        # wrap it and add it to the final string
        wrapped_lines.append(color_start + line + color_end)

    # rejoin strings using newline
    final_str = "\n".join(wrapped_lines)

    print(final_str, sep=sep, end=end, file=file, flush=flush)


# ------------------------------------------------------------------------------
# Print a string if the debug param is True
# ------------------------------------------------------------------------------
def printd(*values, sep=" ", end="\n", file=None, flush=False):
    """
    Print a string if the debug param is True

    Args:
        *values: A variable number of string arguments
        sep: The string used to join *values (default: ' ')
        end: The character(s) to print after the *values (default:'\n')
        file: The file object to print to or, if None, print to stdout
        (default: None)
        flush: Whether to force the output buffer to write immediately, rather
        than waiting for it to fill


    This function is really handy for me when I run a program in debug mode. It
    just lets me wrap prints in context-aware statements
    """

    if B_DEBUG:
        printc(
            *values,
            sep=sep,
            end=end,
            file=file,
            flush=flush,
            fg=C_FG_RED,
            bold=True,
        )


# -)
