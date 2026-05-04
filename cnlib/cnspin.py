# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename:                                                       |     ()     |
# Date    : 05/04/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A decorator to wrap a function in code to print a spinner somewhere in a status
line.
Heavily inspired by Dave Eddy (https://www.youtube.com/@yousuckatprogramming)
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from cmd import Cmd
import threading
from time import sleep

from pprint import pprint

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

    Args:
        strs: the list of strings to rotate through when animating the spinner
        interval: the amount of time, in sconds, between animation frames
        (accepts fraction time)

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
def _fix_len(msg: str, strs: list[str], last_msg: str) -> tuple[list[str], str]:
    """
    Make sure all messages are the same length

    Args:
        msg: The format string to display
        strs: the list of strings to rotate through when animating the spinner
        last_msg: The last message do display before restoring cursor

    Returns:
        (list, str)
            list: the final list of formatted, padded strings
            str: the final padded last_msg

    A private function to make sure all message strings are the same length by
    padding them with trailing spaces.
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
    len_last = len(last_msg)
    len_max = max(len_max, len_last)

    # NB: len_max is now the length of the longest string after formatting
    # (including last_msg)

    # --------------------------------------------------------------------------
    # pad strings and last_msg

    # then we make a list of formatted/padded strings
    new_strs = [item.ljust(len_max) for item in new_strs]

    # now we pad the last_msg
    new_last_msg = last_msg.ljust(len_max)

    # --------------------------------------------------------------------------

    # and we outie
    return new_strs, new_last_msg


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main method
# ------------------------------------------------------------------------------
def spin(msg: str, strs: list[str], last_msg: str, interval: float):
    """
    Main method

    Arguments:
        msg: The format string to display
        strs: the list of strings to rotate through when animating the spinner
        last_msg: The last message do display before restoring cursor
        interval: the amount of time, in sconds, between animation frames
        (accepts fraction time)

    Use a format string like 'Downloading file{}' and a list of strings like
    '["", ".", "..", "..."]' and you will get a nice animated ellipsis. For the
    final message, use something like 'Downloading file: Done'. Note that
    formatting works better if the strings in sts are all the same length,
    especially when the spinner is not at the end of the line.

    This function will calculate the shortest space-padded string needed to
    clear the line each time the spinner redraws.
    """

    # the name of the internal decorator and the name of the function we are
    # decorating
    def inner_spin(function):

        # what to do before and after the real function
        def wrapper(*args, **kwargs):

            # NB: we need a try to capture as many errors as possible so we can
            # restore the cursor
            try:

                # hide cursor
                print("\033[?25l")

                # rewrite array and last_msg to contain formatted/padded strs
                strs_pad, last_msg_pad = _fix_len(msg, strs, last_msg)

                # start spinner on new thread
                t_spin = threading.Thread(
                    target=_spinner, args=(strs_pad, interval)
                )
                t_spin.start()

                # do the original function with same args
                function(*args, **kwargs)

                # set kill spinner flag
                global STOP_SPINNER
                STOP_SPINNER = True

                # wait for thread before show cursor (prints newline?)
                t_spin.join()

                # NB: this is because turning the cursor back on prints a
                # newline
                print(last_msg_pad)
                print("\033[?25h")  # show cursor

            # failsafe (not good enough?)
            except Exception as e:
                print("\033[?25h")  # show cursor
                print(e)

        # this gives the new wrapped code to inner_spin
        return wrapper

    # this gives the new wrapped code to spin
    return inner_spin


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function

    # theme 1
    # MSG = "Downloading new apod dict... {}"
    # CHARS = ["|", "/", "-", "\\"]  # all lens 1
    # LAST_MSG = "Downloading new apod dict... Done"
    # INTERVAL = 0.2

    # theme 2
    # MSG = "Downloading new apod dict{}"
    # CHARS = ["    ", ".   ", "..  ", "... "]  # all lens 4
    # LAST_MSG = "Downloading new apod dict... Done"
    # INTERVAL = 0.2

    # theme 3
    MSG = "Downloading new apod dict{}"
    CHARS = ["", ".", "..", "..."]  # different lens
    LAST_MSG = "Downloading new apod dict... Done"
    INTERVAL = 0.2

    # --------------------------------------------------------------------------

    @spin(MSG, CHARS, LAST_MSG, INTERVAL)
    def do_long(interval):

        # NB: printing in this method is sketchy, probably don't do it
        # print("do_long start", end="\r")
        sleep(interval)
        # print("do_long end", end="\r")

    do_long(5)

# -)
