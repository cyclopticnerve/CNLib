# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename:                                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The template file for a decorator with no parameters.
THIS IS A TEMPLATE, NOT A BASE CLASS!!!
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
        func: The function to be decorated

    Returns:
        The nested function "wrapper", which is called instead of the decorated
        function

    Do some stuff before/after the original function. The original function is
    implied as a parameter when used as "@decorator" immediately before the
    function declaration.
    """

    # do stuff before decorator
    print("decorator before")

    # match any function signature
    def wrapper(*args, **kwargs):
        """
        The one that does all the work

        Arguments:
            *args: List of all args that doe not have keywords (positional
            args)
            **kwargs: List of all args that do have keywords (foo=bar,
            etc.)
        """

        # do stuff before wrap
        print("wrap before")

        # ------------------------------------------------------------------

        print("mod args here")

        args = list(args)
        args[0] = 10
        args = tuple(args)

        # ------------------------------------------------------------------

        print("mod kwargs here")

        # ------------------------------------------------------------------

        key="_foob"

        kwargs = dict(kwargs)
        kwargs[key] = 7
        kwargs = dict(kwargs)

        # ------------------------------------------------------------------

        # do real call with args and store res
        print(f"call real:{args}, {kwargs}")
        res = func(*args, **kwargs)

        # do stuff before res
        print("res before:", res)

        # modify res here
        print("modify res here")

        res = 42

        # do stuff after res
        print("res after:", res)

        # do stuff after wrap
        print("wrap after")

        # we are done, return func res
        return res

    # do stuff after decorator
    print("decorator after")

    # return wrap func as new pointer for a_func
    # NB: this is the function that ultimately gets called
    return wrapper


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # --------------------------------------------------------------------------
    # decoration declaration

    # NB: this is equivalent to writing:
    # _a_func = decorator(_a_func) -> wrapper
    # so now calling _a_func actually calls wrapper, which calls the original
    # _a_func (passing args and returning result, same as original _a_func)
    # note that arguments are accessed in the wrapper function as *args,
    # **kwargs
    # but are passed to the real function as normal
    # decorator returns a function (wrapper), which, when called, runs the real
    # function
    # it uses arguments and return values just as the real function would
    @decorator
    def _a_func(x: float, y: float, _foob=0) -> float:
        """docstring"""
        return x * y

    # --------------------------------------------------------------------------
    # run test

    print("----------------")
    print("real func before")
    print(_a_func(6, 7))
    print("real func after")

# -)
