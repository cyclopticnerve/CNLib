# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnspinner.py                                          |     ()     |
# Date    : 05/10/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A decorator to print a spinner somewhere in a status line
Heavily inspired by Dave Eddy (https://www.youtube.com/@yousuckatprogramming)

For decorator templates, see cndecorator.py and cndecorator_params.py in this
directory.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from threading import Thread, Event
from time import sleep
from typing import Any, Callable

# venv imports
from cnlib import cnfunctions as F

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Strings

# the current message, reset each time
S_MSG = ""

# dictionary keys
S_KEY_FRAMES = "frames"
S_KEY_INTERVAL = "interval"
S_KEY_DONE = "done"
S_KEY_FAIL = "fail"
S_KEY_MSG = "msg"
S_KEY_FG = "fg"
S_KEY_BG = "bg"
S_KEY_BOLD = "bold"

# terminal escape commands
S_HIDE_CURSOR = "\033[?25l"
S_SHOW_CURSOR = "\033[?25h"

# ------------------------------------------------------------------------------
# Dictionaries

# default spinner options

# frames:   List of strings to rotate through when animating the spinner
# interval: Amount of time, in seconds, between animation frames (accepts
#           fractional time)
# done:     Dict of stuff to print when done
# fail:     Dict of stuff to print when failed
# msg:      What to print after last_msg
# fg:       Foreground color for pass/fail
# bg:       Background color for pass/fail
# bold:     True for bold in pass/fail

D_SPIN = {
    S_KEY_FRAMES: ["", ".", "..", "... "],
    S_KEY_INTERVAL: 0.5,
    S_KEY_DONE: {
        S_KEY_MSG: "Done",
        S_KEY_FG: F.C_FG_GREEN,
        S_KEY_BG: F.C_BG_NONE,
        S_KEY_BOLD: True,
    },
    S_KEY_FAIL: {
        S_KEY_MSG: "Failed",
        S_KEY_FG: F.C_FG_RED,
        S_KEY_BG: F.C_BG_NONE,
        S_KEY_BOLD: True,
    },
}

# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The code to draw the spinner on a background thread
# ------------------------------------------------------------------------------
def _thread_spin(evt: Event, msgs: list[str], interval: float):
    """
    The code to draw the spinner on a background thread

    Arguments:
        evt: Event object to control stopping the thread
        msgs: List of strings to rotate through when animating the spinner
        interval: Amount of time, in seconds, between animation frames
        (accepts fractional time)

    This is a private function that handles the animation of the line.
    Note that lines[] are formatted by _fix_len() from the msg strings and
    frames passed to spin().
    """

    # start spinner and run until flag
    while not evt.is_set():

        # for each string in strs
        for msg in msgs:

            # print message and put cursor back at start
            print(msg, end="\r")

            # wait for interval
            sleep(interval)


# ------------------------------------------------------------------------------
# Make sure all messages are the same length
# ------------------------------------------------------------------------------
def _fix_len(msg: str) -> list[str]:
    """
    Make sure all messages are the same length

    Arguments:
        msg: The format string to use as the mesage

    Returns:
        A tuple consisting of:
            list: A list of formatted, padded strings

    A private function to make sure all message strings are the same length by
    padding them with trailing spaces. This is done to ensure the previous
    message gets completely overwritten, leaving no artifacts.

    This function will calculate the shortest space-padded strings needed to
    clear the line each time the spinner redraws.
    """

    # get the strings of interest from the options dict
    frames = D_SPIN[S_KEY_FRAMES]

    # NB: this should be more flexible
    msg = msg + "{}"
    msgs = [msg.format(a_msg) for a_msg in frames]

    # get len_max
    len_max = 0

    # loop through strs
    for a_msg in msgs:
        len_new = len(a_msg)
        len_max = max(len_max, len_new)

    # make a list of formatted/padded strings
    msgs = [a_msg.ljust(len_max) for a_msg in msgs]

    # --------------------------------------------------------------------------

    # and we Audi 5000
    return msgs


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Decoration implementation with params
# ------------------------------------------------------------------------------
def spin(msg: str) -> Callable:
    """
    Decoration implementation with params

    Arguments:
        msg: The format string to use as the message

    Returns:
        The function that matches <some_name>(some_func), which in turn returns
        wrapper(*args, ** kwargs), which is called instead of the decorated
        function

    This function is the main entry point for the decorator, passing the
    function signature and parameters as they are called in code, as a hidden
    first param. It also passes the parameters passed to the decorator.
    """

    # NB: do stuff before deco

    # --------------------------------------------------------------------------
    # Decoration implementation with no parameters
    # --------------------------------------------------------------------------
    def spin2(func: Callable) -> Callable:
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

        # ----------------------------------------------------------------------
        # The one that does all the work
        # ----------------------------------------------------------------------
        def wrapper(*args, **kwargs) -> tuple[bool, Any]:
            """
            The one that does all the work

            Arguments:
                *args: List of all args that do not have keywords (positional
                args)
                **kwargs: Dict of all args that do have keywords (foo=bar,
                etc.)

            Returns:
                A tuple consisting of:
                    bool: A boolean indicating whether the step was successful
                    Any: An error object if the step failed, or any value
                    (including None) if the call succeeded

            This method does the real work, performing the before-call code,
            the actual function, and the after-call code.
            """

            # rewrite array to contain formatted/padded strs
            msgs = _fix_len(msg)

            # create thread outside of try so we can get it in except
            evt = Event()
            t_spin = Thread(
                target=_thread_spin, args=(evt, msgs, D_SPIN[S_KEY_INTERVAL])
            )

            # default return values
            res = False
            obj = None

            # NB: we need a try to capture as many errors as possible so we can
            # restore the cursor
            try:

                # --------------------------------------------------------------
                # do stuff before call

                # hide cursor
                print(S_HIDE_CURSOR, end="\r")

                # --------------------------------------------------------------
                # start spinner on new thread
                t_spin.start()

                # --------------------------------------------------------------
                # do real call with args and store res
                res, obj = func(*args, **kwargs)

                # --------------------------------------------------------------
                # set flag and wait for thread
                evt.set()
                t_spin.join()

                # --------------------------------------------------------------
                # do stuff after call

                # print last msg
                last_msg = msgs[-1]
                print(last_msg, end="")

                # print done/fail
                if res:
                    # print green done
                    a_dict = D_SPIN[S_KEY_DONE]
                    F.printc(
                        a_dict[S_KEY_MSG],
                        fg=a_dict[S_KEY_FG],
                        bg=a_dict[S_KEY_BG],
                        bold=a_dict[S_KEY_BOLD],
                    )
                else:
                    # print red fail/error
                    a_dict = D_SPIN[S_KEY_FAIL]
                    F.printc(
                        a_dict[S_KEY_MSG],
                        fg=a_dict[S_KEY_FG],
                        bg=a_dict[S_KEY_BG],
                        bold=a_dict[S_KEY_BOLD],
                    )
                    if obj and F.B_DEBUG:
                        print(str(obj))

                # show cursor
                print(S_SHOW_CURSOR, end="")

            # failsafe (not good enough?)
            except Exception as e:  # pylint: disable=W0718

                # make sure we stop the thread
                evt.set()
                t_spin.join()

                # show cursor and print error
                print(S_SHOW_CURSOR, end="")  # show cursor
                F.printd(str(e))

            # throw away results
            return (res, obj)

        # return wrap func as new pointer for a_func
        # NB: this is the function that ultimately gets called
        return wrapper

    # return inner here
    return spin2


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # --------------------------------------------------------------------------

    DEBUG = True
    F.B_DEBUG = DEBUG
    ERR = False

    @spin("Downloading file")
    def do_long(interval):
        """docstring"""

        # uncaught exception
        # raise IOError("test")

        sleep(interval)

        # caught exception
        try:
            if ERR:
                raise IOError("test")
            return (True, None)
        except IOError as e:
            if DEBUG:
                return (False, e)
            return (False, None)

    # --------------------------------------------------------------------------

    # do the thing
    do_long(5)

# -)
