# ------------------------------------------------------------------------------
# Project : Configurator                                           /          \
# Filename: configurator.py                                       |     ()     |
# Date    : 10/27/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import json
import re


# ------------------------------------------------------------------------------
# Public methods
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Load the defaults dict, apply user values, and perform substitutions
# ------------------------------------------------------------------------------
def load(dict_defs, dict_user=None, dict_subs=None, allow_conflicts=True,
         allow_user_extras=False):

    """
        Load the defaults dict, apply user values, and perform substitutions

        Args:
            dict_defs: the dict of defaults
            dict_user [dict]: the dict of user settings
            dict_subs [dict]: the dict of substitutions to perform
                Dict must be in the form of: {"${SUB}": "substitution_string"}
            allow_conflicts [bool]: if True, type conflicts in values are
                resolved in favor of defaults. if False, any type conflict
                raises an Exception
            allow_user_extras [bool]: if True, user keys which do not appear in
                defaults are kept. if False, extraneous user keys are removed

        Returns:
            [dict]: a dict containing all merged keys and values, with
            substitutions applied

        This function combines the defaults dict with the user dict, returning
        a third dict containing the union of those two dicts. It also performs
        substitutions using the specified dict_subs. Type conflicts between the
        defaults dict and the user dict are handled by the allow_conflicts
        parameter. User dict keys that are not present in the defaults dict
        will be kept (but obviously not type-checked) if the allow_user_extras
        parameter is True, otherwise they are discarded.
    """

    # the default return dict
    # NB: if anything goes wrong, this is the dict we will return
    dict_res = dict(dict_defs)

    # validate dict_defs
    _validate_json(dict_defs)

    # apply user values
    if dict_user is not None:

        # validate and apply dict_user
        _validate_json(dict_user)
        dict_res = _set_defaults(dict_defs, dict_user, allow_conflicts,
                                 allow_user_extras)

    # apply substitutions
    if dict_subs is not None:

        # validate and apply dict_subs
        _validate_json(dict_subs)
        dict_res = _set_substitutions(dict_res, dict_subs)

    # return the final dict
    return dict_res


# ------------------------------------------------------------------------------
# Private methods
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Validate the JSON of the specified dict
# ------------------------------------------------------------------------------
def _validate_json(dict_json):

    """
        Validate the JSON of the specified dict

        Parameters:
            dict_json [dict]: the dict to validate

        Raises:
            Exception(str): if not valid JSON

        This method validates the specified dict by converting it to a string
        and then back to a dictionary.
    """

    # turn dict to string
    str_json = json.dumps(dict_json)

    try:

        # load json from string (the validation happens in the json module)
        json.loads(str_json)

    # throw error if not valid
    except Exception as error:
        raise Exception(f'JSON validation error: {error}')


# ------------------------------------------------------------------------------
# Merge a user settings dict into a default settings dict
# ------------------------------------------------------------------------------
def _set_defaults(dict_defs, dict_user, allow_conflicts, allow_user_extras,
                  dict_res=None, key_path=''):

    """
        Merge a user settings dict into a default settings dict

        Paramaters:
            dict_defs [dict]: the dict containing the default values
            dict_user [dict]: the dict containing user values to be applied over
                defaults
            allow_conflicts [bool]: if True, type conflicts in values are
                resolved in favor of defaults. if False, any type conflict
                raises an Exception
            dict_res [dict]: the resulting dict to be returned
            key_path [str]: the path to the current key, used to track conflicts

        Returns:
            [dict]: a dict containing all merged keys and values

        Raises:
            Exception(str): if either dict_defs or dict_user is not a dict
            Exception(str): if allow_conflicts is False and a type conflict
                occurs

        This method does the heavy lifting of merging two dictionaries and
        checking for type mismatches and extraneous keys. It is also recursive
        to allow for a deep merge in the case that a value is also a dictionary.
    """

    # check that we only pass dicts with at least one key
    if not isinstance(dict_defs, dict):
        raise Exception('Parameter dict_defs is not a dict')
    if not isinstance(dict_user, dict):
        raise Exception('Parameter dict_user is not a dict')

    # start with defs
    if dict_res is None:
        dict_res = dict(dict_defs)

    # for each entry in user dict
    for key in dict_user.keys():

        # if that entry is also in defaults (this is a good thing)
        if key in dict_defs.keys():

            # check that the user value type is same type as defs value type
            user_val_type = type(dict_user[key])
            defs_val_type = type(dict_defs[key])

            # if types match (this is a good thing)
            if user_val_type == defs_val_type:

                # if both types are a dict (and match)
                if isinstance(dict_user[key], dict):

                    # create a temp path (very important for recursion...)
                    # NB: don't change key_path in this recursion, or else we
                    # can't get back to it when un-recursing (if that makes any
                    # sense)
                    key_path_str = key_path + '/' + str(key)

                    # recurse using current values
                    _set_defaults(dict_defs[key], dict_user[key],
                                  allow_conflicts, allow_user_extras,
                                  dict_res[key], key_path_str)

                # TODO: lists? merge? overwrite?
                # elif isinstance(dict_user[key], list):
                
                # if both types are not dict or list (but still match)
                else:

                    # copy user val to defs val
                    dict_res[key] = dict_user[key]

            # oh nos! types don't match
            else:

                # what to do? don't allow conflicts = KABOOM!
                if not allow_conflicts:

                    # create a temp path (very important for recursion...)
                    # NB: don't change key_path in this recursion, or else we
                    # can't get back to it when un-recursing (if that makes any
                    # sense)
                    key_path_str = key_path + '/' + str(key)

                    # raise an Exception with the key path and the two types
                    raise Exception(
                        f"Conflict at {key_path_str}, " +
                        f"defs type = {defs_val_type}, " +
                        f"user type = {user_val_type}"
                    )

                # NB: if we DO allow conflicts to pass, nothing happens and the
                # default value remains unchanged (thereby defaulting to defs)

        # allow extra keys to remain
        elif allow_user_extras:
            dict_res[key] = dict_user[key]

    # return the final dict
    return dict_res


# --------------------------------------------------------------------------
# Perform substitutions for keys/values in config file
# --------------------------------------------------------------------------
def _set_substitutions(dict_in, dict_subs):

    """
        Perform substitutions for keys/values in config file

        Parameters:
            dict_in [dict]: the dict where substitutions are to be performed
            dict_subs [dict]: the dict of substitutions to perform

        Returns:
            [dict]: the dict with substitutions performed

        Raises:
            Exception(str): if key is not a valid substitution key

        This method performs substitutions in the final dict's keys and values.
        The dict must be in the form of: {"${SUB}": "substitution_string"}.
        Note that if a replacement results in a duplicate key, the last key
        that was defined (after substitutions) will supersede any previous keys
        (see tests/test.py for more info).
        Also note that substitutions are not recursive, so
        {
            "${FOO}": "bar",
            "${BAZ}": "${FOO}"
        }
        will *not* do what you think it will. However, 
        {
            "${BAZ}": "${FOO}",
            "${FOO}": "bar"
        }
        will replace "${BAZ}" with "${FOO}", which will be replaced by "bar".
        
    """

    # TODO: replace vals in dict with keys to make recursive

    # the default return dict
    # NB: if anything goes wrong, this is the dict we will return
    dict_res = dict(dict_in)

    # convert dict to string
    dict_str = json.dumps(dict_in)

    # do string replace
    for key, val in dict_subs.items():

        # test if key is a valid sub
        if re.match(r"\${.*}", key):
        
            # if it is valid, do whole string replace
            dict_str = dict_str.replace(key, val)
        else:
            raise Exception(f'Substitution error: {key} incorrect format')

    # convert string to dict
    dict_res = json.loads(dict_str)

    # return dict with replacements
    return dict_res

# -)
