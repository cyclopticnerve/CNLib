# ------------------------------------------------------------------------------
# Project : CNLib                                                 /          \
# Filename: cndecorator.py                                        |     ()     |
# Date    : 05/10/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The base file for a decorator with no parameters
"""

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Decoration implementation with no parameters
# ------------------------------------------------------------------------------
def decorator(func):
    """
    Decoration implementation with no parameters

    Arguments:
        func: The object representation of the function to be decorated (name,
        params/types, return type)

    Returns:
        The function that matches wrapper(*args, ** kwargs), which is called
        instead of the decorated function

    Do some stuff before and after calling the original function.
    """

    # do stuff before decorator
    print("decorator before")

    # match any function signature
    def wrap(*args, **kwargs):

        # do stuff before wrap
        print("wrap before")

        # do real call with args and store res
        print(f"call real:{args}, {kwargs}")
        res = func(*args, **kwargs)

        # do stuff before res
        print("res before:", res)

        # modify res here
        print("modify res here")

        # do stuff after res
        print("res after:", res)

        # do stuff after wrap
        print("wrap after")

        # we are done
        return res

    # do stuff after decorator
    print("decorator after")

    # return wrap func as new pointer for a_func
    # NB: this is the function that ultimately gets called
    return wrap


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # --------------------------------------------------------------------------
    # decoration declaration

    @decorator
    def a_func(x: float, y: float) -> float:
        """docstring"""
        return x * y

    # --------------------------------------------------------------------------
    # run test

    print("-")
    print("func before")
    print(a_func(6, 7))
    print("func after")

# -)
