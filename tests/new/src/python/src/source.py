"""docstring"""

# NB: see
from tests.new.src.python.helpers.i18n import _, _p

#-------------------------------------------------------------------------------
# basic usage

string1 = _("string1")
print(string1)

# it also works in nested parentheses
print(_("string2"))

#-------------------------------------------------------------------------------
# beware empty translations!

# the empty translatable string '_("")' is reserved in pot/po files to mark the
# header. it may or may not break the pot/po file, depending on certain
# circumstances, which we will not discuss. suffice to say, DON'T USE IT.
# xgettext will warn if it finds an empty translatable string, but it will
# still create the broken pot file.

# string2 = _("")  # this is bad!

#-------------------------------------------------------------------------------
# comments (tags)

# a typical comment
string3 = _("string3")
print(string3)

# comment (do not show when tag is used)
# this line is included, but only the part after the tag I18N:
# I18N: shows when tag = "I18N:"

# the empty line above is ignored
# this line has no tag, but it also appears in the pot file
print(_("string4"))

# there are three possible options for comments:
# 1. if '-c' is not present, ignore all comments
# 2. if only '-c' is present, show all comments
# 3. if '-cTAG' is present, show only lines after first occurrence of 'TAG'

# NB: comments are considered all lines before a translatable string that start
# with '#', or empty lines. empty lines do not appear in the output. when '-c'
# is used, parsing stops when the first non-empty, non-comment line is found.
# when using '-cTAG', parsing stops when the earliest occurrence of "TAG" is
# found, or a non-empty, non-comment line is found.

# ------------------------------------------------------------------------------
# plurals
# pot should not contain plurals info, only po files (lang dependant)

# N = 0
# N = 1
N = 2

# ngettext returns one or another string depending on the value of N
# NB: f-strings are a no go here, use old-skool formatting
# order of operations: get format string first, THEN apply formatting
# NB: handling more (or less, jp=1) pluralized forms is on the translator.
# just make sure you have two strings (to give the translator a general idea)
# and an integer. even better, add a tag!
# I18N: format param '{}' is the number of items the user has
# plural_str = t.ngettext("I have {} item", "I have {} items", N)
# NB: optional, see top of file
plural_str = _p("I have {} item", "I have {} items", N)

# then we format the string using the returned format string and N
print(plural_str.format(N))

# for non-integer strings
# NB: we separate the strings to get separate comments
# I18N: non-integer single
single_str2 = _("One item")
# I18N: format param '{}' is the number of items the user has
plural_str2 = _("{} items")
# NB: did you know you could put expressions in print? CUZ I DIDN'T!!!'
# ternary operations FTW!
print(single_str2.format(N) if N == 1 else plural_str2.format(N))

#-------------------------------------------------------------------------------
# format strings

STRING = "Hello"
LENGTH = len(STRING)

# translator needs to know what vals are at those positions
# I18N: param '{0}' is the string(str) and param '{1}' is the length(int)
f_str = _("The word '{0}' has {1} characters")
# In other lang
# f_str = f"There are {1} characters in the word '{0}'"
print(f_str.format(STRING, LENGTH))
