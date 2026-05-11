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
import threading
from time import sleep

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# used to kill spinner thread
STOP_SPINNER = False

# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The code to draw the spinner on a background thread
# ------------------------------------------------------------------------------
def _spinner(strs: list[str], interval: float):
    """
    The code to draw the spinner on a background thread

    Arguments:
        strs: List of strings to rotate through when animating the spinner
        interval: Amount of time, in seconds, between animation frames
        (accepts fractional time)

    This is a private function that handles the animation of the line.
    """

    # start spinner and run until flag
    while not STOP_SPINNER:

        # for each string in strs
        for string in strs:

            # print message and put cursor at start
            print(string, end="\r", flush=True)

            # wait for interval
            sleep(interval)


# ------------------------------------------------------------------------------
# Make sure all messages are the same length
# ------------------------------------------------------------------------------
def _fix_len(
    msg: str, strs: list[str], last_msg: str
) -> tuple[list[str], str]:
    """
    Make sure all messages are the same length

    Args:
        msg: Format string to display
        strs: List of strings to rotate through when animating the spinner
        last_msg: Last message do display before restoring cursor (Usually has
        no animation, shows a 'done' message)

    Returns:
        list: A list of formatted, padded strings
        str: The final padded last_msg

    A private function to make sure all message strings are the same length by
    padding them with trailing spaces. This is done to ensure the previous
    message gets completely overwritten, leaving no artifacts.
    """

    # start value for max
    len_max = 0

    # --------------------------------------------------------------------------
    # format all strings

    # first we make a list of formatted strings
    new_strs = [msg.format(item) for item in strs]

    # --------------------------------------------------------------------------
    # get len_max

    # loop through strs
    for string in new_strs:
        len_new = len(string)
        len_max = max(len_max, len_new)

    # get max using last_msg
    len_new = len(last_msg)
    len_max = max(len_max, len_new)

    # NB: len_max is now the length of the longest string after formatting
    # (including last_msg)

    # --------------------------------------------------------------------------
    # pad strings and last_msg

    # then we make a list of formatted/padded strings
    strs_pad = [item.ljust(len_max) for item in new_strs]

    # now we pad the last_msg
    last_pad = last_msg.ljust(len_max)

    # --------------------------------------------------------------------------

    # and we outie
    return strs_pad, last_pad


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Decoration implementation with params
# ------------------------------------------------------------------------------
def spin(msg: str, strs: list[str], last_msg: str, interval: float):
    """
    Decoration implementation with params

    Args:
        msg: The format string to display
        strs: The list of strings to rotate through when animating the spinner
        last_msg: The last message do display before restoring cursor
        interval: The amount of time, in seconds, between animation frames
        (accepts fractional time)

    Returns:
        The method that matches <some_name>(some_func), which in turn returns
        wrapper(*args, ** kwargs), which is called instead of the decorated
        function

    Use a format string like 'Downloading file{}' and a list of strings like
    '["", ".", "..", "..."]' and you will get a nice animated ellipsis. For the
    final message, use something like 'Downloading file: Done'. Note that
    formatting works better if the strings in sts are all the same length,
    especially when the spinner is not at the end of the line.

    This function will calculate the shortest space-padded string needed to
    clear the line each time the spinner redraws.
    """

    # do stuff before deco

    # rewrite array and last_msg to contain formatted/padded strs
    strs_pad, last_pad = _fix_len(msg, strs, last_msg)

    # --------------------------------------------------------------------------
    # Decoration implementation with no parameters
    # --------------------------------------------------------------------------
    def _spin2(func):
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

        # match any function signature
        def _wrapper(*args, **kwargs):

            # default result
            res = None

            # NB: we need a try to capture as many errors as possible so we can
            # restore the cursor
            try:

                # do stuff before call
                # hide cursor
                print("\033[?25l", end="\r")

                # start spinner on new thread
                t_spin = threading.Thread(
                    target=_spinner, args=(strs_pad, interval)
                )
                t_spin.start()

                # do real call with args and store res
                res = func(*args, **kwargs)

                # do stuff after call

                # set kill spinner flag
                global STOP_SPINNER  # pylint: disable=W0603
                STOP_SPINNER = True

                # wait for thread before show cursor (prints newline?)
                t_spin.join()

                # NB: this is because turning the cursor back on prints a
                # newline
                print(last_pad)
                print("\033[?25h", end="\r")  # show cursor

            # failsafe (not good enough?)
            except Exception as e:  # pylint: disable=W0718
                print("\033[?25h")  # show cursor
                print(e)

            # we are done
            return res

        # return wrap func as new pointer for a_func
        # NB: this is the function that ultimately gets called
        return _wrapper

    # return inner here
    return _spin2


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # some constants to pass to the spinner
    MSG = "Downloading new apod dict{}"
    CHARS = ["", ".", "..", "..."]  # different lens
    LAST_MSG = "Downloading new apod dict... Done"
    INTERVAL = 0.2

    # --------------------------------------------------------------------------

    # the wrapped function
    @spin(MSG, CHARS, LAST_MSG, INTERVAL)
    def _do_long(interval):
        """docstring"""

        # NB: printing in this method is sketchy, probably don't do it
        # print("do_long start", end="\r")
        sleep(interval)
        # print("do_long end", end="\r")

    _do_long(5)

# -)
