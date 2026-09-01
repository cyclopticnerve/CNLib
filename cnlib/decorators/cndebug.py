# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cndebug.py                                            |     ()     |
# Date    : 08/25/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A decorator to print a message whenever we enter or exit a method or function.
Useful in debugging, maybe.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# venv imports
from cnlib import cnfunctions as F

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Print the enter/result/exit messages
# ------------------------------------------------------------------------------
def debug(func):
    """
    Print the enter/result/exit messages
    """

    # NB: at the end of the day, this is what gets run
    def wrapper(*args, **kwargs):
        F.printd(f"debug enter: {func.__name__}")
        res = func(*args, **kwargs)
        # NB: F.pf returns a formatted string, BUT DOES NOT PRINT
        F.printd(f"debug result: {F.pf(res)}")
        F.printd(f"debug exit: {func.__name__}")
        return res

    return wrapper


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # make sure F.printd does something
    F.B_DEBUG = True

    # --------------------------------------------------------------------------
    # function somewhere to be dec'd

    @debug
    def my_func(x, y):
        """docstring"""
        # return x * y
        return {"foo": x, "bar": y}

    # my_func = debug(my_func)
    # my_func(*args, **kwargs) = debug.wrapper(*args, **kwargs)

    # --------------------------------------------------------------------------
    # use the func somewhere
    # my_func(6, 7)
    print(my_func(6, 7))

# -)
