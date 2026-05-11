# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cndecorator_params.py                                 |     ()     |
# Date    : 05/10/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The base file for a decorator with parameters

"""

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Decoration implementation with params
# ------------------------------------------------------------------------------
def decorator(x, y):
    """
    Decoration implementation with params

    Arguments:
        x: A parameter to the outer decorator
        y: A parameter to the outer decorator

    Returns:
        The method that matches <some_name>(some_func), which in turn returns
        wrapper(*args, ** kwargs), which is called instead of the decorated
        function

    Do the function with the specified parameters and return the result.
    """

    # do stuff before decorator
    print("decorator before")

    # use x, y here
    print("x:", x, "y:", y)

    # --------------------------------------------------------------------------
    # Decoration implementation with no parameters
    # --------------------------------------------------------------------------
    def _decorator_inner(func):
        """
        Decoration implementation with no parameters

        Arguments:
            func: The object representation of the function to be decorated
            (name, params/types, return type)

        Returns:
            The function that matches wrapper(*args, ** kwargs), which is
            called instead of the decorated function


        Do some stuff before and after calling the original function.
        """

        # do stuff before decorator_inner
        print("decorator_inner before")

        # match any function signature
        def _wrap(*args, **kwargs):

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

        # do stuff after decorator_inner
        print("decorator_inner after")

        # return wrap func as new pointer for a_func
        # NB: this is the function that ultimately gets called
        return _wrap

    # do stuff after decorator
    print("decorator after")

    # return inner here
    return _decorator_inner


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # --------------------------------------------------------------------------
    # decoration declaration

    @decorator(1, 2)
    def _a_func(x: float, y: float) -> float:
        """docstring"""
        return x * y

    # --------------------------------------------------------------------------
    # run test

    print("-")
    print("func before")
    print(_a_func(6, 7))
    print("func after")

# -)
