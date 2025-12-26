# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cntree.py                                             |     ()     |
# Date    : 08/06/2023                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module creates a tree of the specified directory, with paths being ignored
by the filter list and names being formatted according to the specified
formats. It creates both text and HTML versions. The HTML version has the
ability to display checkboxes that show the state of each item as either
checked, unchecked, or indeterminate, according to their child checkboxes'
values.
"""

# TODO: only do check event on load if item has no children
# start bottom up?

# TODO: empty lines for readability?

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Generate a file tree in text format with the names formatted according to some
# format strings
# ------------------------------------------------------------------------------
class CNTree:
    """
    Generate a file tree in text format with the names formatted according to
    some format strings

    Methods:
        main: Creates a tree from the given start directory, using filter list,
        directory and file formats

    This class builds the tree as a complete string, ready to be printed to
    stdout or a file.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # console/terminal values for the individual prefix/connector chars
    S_CHAR_VERT = "\u2502"  # vertical join (pipe)
    S_CHAR_HORZ = "\u2500"  # horizontal join (full-width dash)
    S_CHAR_TEE = "\u251c"  # tee join (not last item)
    S_CHAR_ELL = "\u2514"  # elbow join (last item)
    S_CHAR_SPACE = " "  # single space char

    # char sequences for the prefix/connector char sets
    # NB: these must always be equal length
    S_PREFIX_VERT = f"{S_CHAR_VERT}{S_CHAR_SPACE}"  # next level ("| ")
    S_PREFIX_NONE = f"{S_CHAR_SPACE}{S_CHAR_SPACE}"  # skip level ("  ")
    S_CONNECTOR_TEE = f"{S_CHAR_TEE}{S_CHAR_HORZ}"  # next sub item ("T-")
    S_CONNECTOR_ELL = f"{S_CHAR_ELL}{S_CHAR_HORZ}"  # last sub item ("L-")

    # the default directory/file name formats
    # NB: NAME alone is used for the top level directory name
    # DIR is used for subdirectories and should have a leading space to
    # separate it from the prefix and/or connector
    # FILE has the same purpose as DIR, but for files (DUH!)
    S_FORMAT_NAME = "$NAME"
    S_FORMAT_DIR = f" {S_FORMAT_NAME}/"
    S_FORMAT_FILE = f" {S_FORMAT_NAME}"

    # error messages
    # NB: format param is dir_prj
    S_ERR_NOT_ABS = "path {} is not absolute"
    # NB: format param is dir_prj
    S_ERR_NOT_DIR = "path {} is not a directory"

    # custom sorting order
    S_SORT_ORDER = "_."  # sort first char of name in this order (above ord)

    # style the html lists
    S_DEF_CSS = """ul {
                list-style-type: none;
                padding-left: 20px;
            }"""

    # --------------------------------------------------------------------------
    # html stuff
    # NB: DO NOT MESS WITH THIS!!!

    # prolog (html/head/style/body)
    # NB: format params are self._css, root name, and root id
    S_HTML_PROLOG = """<!DOCTYPE html>
<html>
<head>
    <style>
        {0}
    </style>
</head>
<body>
    <ul>
        <li>
            <input type="checkbox" id="{2}">
            <label for="{2}">{1}</label>
            <ul>"""

    # epilog (what comes after the checkbox list)
    S_HTML_EPILOG = """
            </ul>
        </li>
    </ul>
    <script>

        // NB: https://codepen.io/girish/pen/BaWMGKp

        // helper func to create a flat array from a NodeList
        nodeArray = (parent, selector) =>
            Array.from(parent.querySelectorAll(selector));

        // get all checkboxes from document
        allChecks = nodeArray(document, 'input[type="checkbox"]');

        // global document listener (add to all inputs)
        addEventListener('change', e => {

            // get object that changed
            check = e.target;

            // if event did not come from a checkbox in our list
            if (allChecks.indexOf(check) === -1)
                return;

            // check/uncheck children based on parent state
            parent = check.parentNode;
            children = nodeArray(parent, 'input[type="checkbox"]');
            children.forEach(child =>
                child.checked = check.checked
            );

            // traverse up from target check
            while (check) {

                // find parent checkbox
                parent = check.closest('ul');
                parent = parent.parentNode;
                parent = parent.querySelector('input[type="checkbox"]');

                // find sibling checkboxes
                siblings = parent.closest('li');
                siblings = siblings.querySelector('ul');
                siblings = nodeArray(siblings, 'input[type="checkbox"]');

                // get checked state of siblings
                // are every or some siblings checked?
                siblingsMap = siblings.map(check => check.checked);
                every = siblingsMap.every(Boolean);
                some = siblingsMap.some(Boolean);

                // check parent if all child siblings are checked
                // set indeterminate if some (not all and not none) are checked
                parent.checked = every;
                parent.indeterminate = !every && every !== some;

                // prepare for next loop
                check = check != parent ? parent : 0;
            }

            // save current state
            save();
        });

        // save current state
        function save() {

            // for each checkbox
            allChecks.forEach(check => {

                // get all the stuff
                id = check.id;
                ind = check.indeterminate;
                checked = check.checked;

                // if it is -, save that
                if (ind) {
                    localStorage.setItem(id, 'ind');

                    // not -, save checked or not
                } else {
                    localStorage.setItem(id, checked);
                }
            });
        };

        // load previous state
        window.onload = function () {

            // for each checkbox
            allChecks.forEach(check => {

                // get all the stuff
                id = check.id;
                ind = localStorage.getItem(id) === 'ind';
                checked = localStorage.getItem(id) === 'true';

                // if it was -, set to -
                if (ind) {
                    check.indeterminate = true

                // if it was not -, set to old state
                } else {
                    check.checked = checked;
                }
            });
        };

    </script>
</body>
</html>

<!-- -) -->
"""

    # start of new entry (file, folder)
    # NB: format params are indent string, self._id, and entry name
    S_ENTRY_OPEN = """
{0}<li>
{0}    <input type='checkbox' id='{1}'>
{0}    <label for='{1}'>{2}</label>
{0}    <ul>"""

    # end of entry (close child list, close entry)
    # NB: format param is indent string
    S_ENTRY_CLOSE = """
{0}    </ul>
{0}</li>"""

    # indent used in <li> to align better
    S_HTML_INDENT = "    "

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initializes the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        start_dir,
        filter_list=None,
        fmt_name="",
        dir_format="",
        file_format="",
        dirs_only=False,
        sort=True,
        sort_files=False,
        ignore_case=False,
        css=None,
    ):
        """
        Initializes the new object

        Args:
            start_dir: String or Path to the root directory of the tree
            filter_list: List of directory/file names to filter out (default:
            None)
            dir_format: Format to use for directories (default:"$NAME/")
            file_format: Format to use for files (default: "$NAME")
            dirs_only: Only list directories (default: False)
            sort: Whether to use the sort_files arg (default: True)
            sort_files: If True, sort files above dirs, or if False, sort dirs
            above files (Ignored if sort is False) (default: False)
            ignore_case: If True, sort entries regardless of case, or if False,
            uppercase alpha characters take precedence (default: False)
            css: Custom css string to use for HTML output

        Creates a tree from the given start directory.

        The start_dir can be an absolute path, a relative path, or a Path
        object, but MUST point to a directory.

        If start_dir does not point to a directory, an OSError will be raised.

        If start_dir == None, an OSError will be raised.

        If start_dir == "", the current directory is used.

        Items in the filter list will be skipped. These items can be relative
        paths, or globs.

        The format strings for directory and file names will have the value
        of "fmt_name" replaced by the directory or file name.

        Example: (assuming "fmt_name" is set to "$NAME")

            dir_format = " [] $NAME/"
            item.name = "Foo"
            result = " [] Foo/"

        Also, leading spaces in dir_format, when applied to the start_dir
        name, will be left-trimmed to make the tree start at the first
        column.

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # set the initial values of properties
        self._start_dir = Path(start_dir)
        if not self._start_dir.is_absolute():
            raise OSError(self.S_ERR_NOT_ABS.format(self._start_dir))
        if not self._start_dir.is_dir():
            raise OSError(self.S_ERR_NOT_DIR.format(self._start_dir))

        # fill in param props
        self._filter_list = filter_list
        if self._filter_list is None:
            self._filter_list = []

        self._fmt_name = self.S_FORMAT_NAME
        if fmt_name and self._fmt_name in fmt_name:
            self._fmt_name = fmt_name

        self._dir_format = self.S_FORMAT_DIR
        if dir_format and self._fmt_name in dir_format:
            self._dir_format = dir_format

        self._file_format = self.S_FORMAT_FILE
        if file_format and self._fmt_name in file_format:
            self._file_format = file_format

        self._dirs_only = dirs_only
        self._ignore_case = ignore_case
        self._sort = sort
        self._sort_files = sort_files

        if not css:
            self._css = self.S_DEF_CSS

        # create private props
        self._root_lead = ""
        self._dir_lead = ""
        self._sort_order = {}
        self._tree = []
        self.text = ""

        # html stuff
        self._level = 2  # initial indent level for html
        self._id = ""  # build a unique id for entries (dot separated path)
        self.html = ""

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Creates a tree from the given start directory, using filter list,
    # directory and file formats
    # --------------------------------------------------------------------------
    def make_tree(self):
        """
        Creates a tree from the given start directory, using filter list,
        directory and file formats

        Returns:
            The current tree as a string

        Raises:
            OSError: If the start_dir parameter is None or does not contain
                a path to a valid directory
        """

        # get filters from globs
        self._get_filter_list()

        # get leads (extra spaces before prefix/connector)
        self._get_leads()

        # create custom sort dictionary
        self._get_sort_order()

        # add root to tree
        self._add_root()

        # enumerate the start dir and add its contents, starting recursion
        self._add_contents(self._start_dir)

        # turn the final tree array into string and html
        self.text = "\n".join(self._tree)
        self.html += self.S_HTML_EPILOG

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Adds the root to the tree
    # --------------------------------------------------------------------------
    def _add_root(self):
        """
        Adds the root to the tree

        This function adds the root item to the tree. It just strips the
        leading blanks to make sure the root is left-aligned.
        """

        # format the root directory name to a display name and add it
        fmt_root = self._dir_format.lstrip()
        rep_name = fmt_root.replace(self._fmt_name, self._start_dir.name)

        # setup text file
        self._tree.append(rep_name)

        # setup html file
        self._id = self._start_dir.name
        self.html += self.S_HTML_PROLOG.format(self._css, rep_name, self._id)

    # --------------------------------------------------------------------------
    # Enumerates the given directory and adds its contents to the tree
    # --------------------------------------------------------------------------
    def _add_contents(self, item, prefix=""):
        """
        Enumerates the given directory and adds its contents to the tree

        Args:
            item: Path object we are adding
            prefix: Current prefix (combination of pipes/blanks) to show
            the level of indentation

        This method is called recursively to build up the visual level of
        indentation, as well as add directory contents to the tree. It does
        a lot of the heavy lifting to determine what gets printed, and how.
        """

        # ----------------------------------------------------------------------
        # fix up items (sort, filter)

        # enum all items in the dir (files and folders) and convert to list
        # NB: we need a list rather than a generator, since we want everything
        # at once (iterdir is a generator, and so yields)
        # this grabs the whole shebang at once
        items = list(item.iterdir())

        # sort everything, first by custom sort (which handles name), then
        # by type (folders first), then removes anything in the filter list
        # it also removes files if the dirs_only value is true

        # the key function's result is used to determine an item's position
        # based on a bubble sort
        # NB: the hidden param to the "key" function is self is an iterator of
        # items i.e:
        # self._sort_by_name([item for item in items])
        items.sort(key=self._sort_by_name)

        # sort works by iterating through a list. this function passes every
        # item through the is_file() test to get its result
        # the item.is_file() might seem backwards, but sort works by placing a
        # false(0) above a true(1), so an item that is NOT a file (ie. a dir,
        # and thus a 0), will be placed above an item that IS a file (and thus
        # a 1)
        if self._sort:
            if not self._sort_files:
                items.sort(key=lambda item: item.is_file())
            else:
                items.sort(key=lambda item: item.is_dir())

        # remove the filtered paths
        items = [item for item in items if item not in self._filter_list]

        # list only dirs if flag is set
        if self._dirs_only:
            items = [item for item in items if item.is_dir()]

        # ----------------------------------------------------------------------
        # get number of files/directories (for determining connector)
        count = len(items)

        # for each entry
        for index, an_item in enumerate(items):

            # ------------------------------------------------------------------
            # text stuff

            # get the type of connector based on position in enum
            connector = (
                self.S_CONNECTOR_TEE
                if index < (count - 1)
                else self.S_CONNECTOR_ELL
            )

            # get format string based on whether it is a dir or file
            fmt = self._dir_format if an_item.is_dir() else self._file_format

            # replace name in format string
            rep_name = fmt.replace(self.S_FORMAT_NAME, an_item.name)

            # add the item to the tree
            self._tree.append(
                f"{self._root_lead}{prefix}{connector}{rep_name}"
            )

            # ------------------------------------------------------------------
            # html stuff

            # increase id level
            self._id += "." + an_item.name

            # increase indent
            self._level += 2
            indent = self.S_HTML_INDENT * self._level

            # add the item to the tree
            self.html += self.S_ENTRY_OPEN.format(indent, self._id, rep_name)

            # ------------------------------------------------------------------
            # recurse

            # if item is a dir
            if an_item.is_dir():

                # --------------------------------------------------------------
                # need a fresh prefix for recursion
                new_prefix = (
                    self.S_PREFIX_VERT
                    if index < (count - 1)
                    else self.S_PREFIX_NONE
                )
                new_prefix += self._dir_lead

                # get whole prefix for next recurse
                new_prefix = prefix + new_prefix

                # recurse with dir and new prefix
                self._add_contents(an_item, new_prefix)

            # ------------------------------------------------------------------
            # html stuff

            # back up id from previous level (+1 for dot)
            self._id = self._id[: -(len(an_item.name) + 1)]

            # unindent for html
            indent = self.S_HTML_INDENT * self._level
            self._level -= 2

            # close the item
            self.html += self.S_ENTRY_CLOSE.format(indent)

    # --------------------------------------------------------------------------
    # Gets the filter_list from paths or globs
    # --------------------------------------------------------------------------
    def _get_filter_list(self):
        """
        Gets the filter_list from paths or globs

        Converts entries in filter_list to absolute Path objects relative
        to start_dir. Globs are acceptable.
        """

        # sanity check
        if self._filter_list is None:
            return

        # do glob
        list_filter = []
        for item in self._filter_list:
            res = list(self._start_dir.glob(item))
            list_filter.extend(res)

        # set result
        self._filter_list = list_filter

    # --------------------------------------------------------------------------
    # Gets the leads (extra spaces) before each entry in the tree
    # --------------------------------------------------------------------------
    def _get_leads(self):
        """
        Gets the leads (extra spaces) before each entry in the tree

        Calculates how many spaces should be presented before each entry in
        the tree. The root folder should have no spaces (left-aligned) and
        each subsequent entry should add the number of spaces in a
        directory's format name. This allows us to align the connector with
        the first character of the FORMAT_NAME variable, skipping things like
        checkbox brackets.
        """

        # get the leads (extra indents to line up the pipes/tees/ells)
        # NB: we don't care about file leads, nothing goes under a file

        # get the root's format with no leading spaces
        root_fmt = self._dir_format.lstrip()

        # set root lead as string
        root_lead_count = root_fmt.find(self.S_FORMAT_NAME)
        self._root_lead = " " * root_lead_count

        # set directory lead as string
        dir_lead_count = self._dir_format.find(self.S_FORMAT_NAME)
        self._dir_lead = " " * dir_lead_count

    # --------------------------------------------------------------------------
    # Gets the sort order for custom sorting by name
    # --------------------------------------------------------------------------
    def _get_sort_order(self):
        """
        Gets the sort order for custom sorting by name

        This just fixes a personal quirk of mine. The default sorting order
        in Python sorts names starting with a dot (.) above a name starting
        with an underscore (_) (as per string.printable), which for me is
        dependant on my locale, en_US, YMMV. This does not match my IDE,
        VSCode, and I want the tree to match my File Explorer in my IDE. So
        to fix this, I created a custom sorter that reverses that. It's not
        really necessary, but it does the job.

        This function creates a dict in the form of:
        {char:index[, ...]}
        where:
        char is the character in the SORT_ORDER string
        index is the ordinal of that char (starting at the lowest negative
        ordinal)
        so that:
        SORT_ORDER = "_."
        results in:
        self._sort_order = {"_": -2, ".": -1}

        most of this came from:
        https://stackoverflow.com/questions/75301122/how-can-i-change-how-python-sort-deals-with-punctuation
        """

        # get length of string to count backwards
        sort_len = len(self.S_SORT_ORDER)

        # for each char in string
        for index, char in enumerate(self.S_SORT_ORDER):
            # make a dict entry for the char and its new ord
            self._sort_order[char] = index - sort_len

    # --------------------------------------------------------------------------
    # Sorts items in the item list according to the item name
    # --------------------------------------------------------------------------
    def _sort_by_name(self, item):
        """
        Sorts items in the item list according to the item name

        Args:
            item: Path object to sort

        Returns:
            The index of the sorted item

        Sorts items in the item list according to the item name, using a simple
        bubble sort (i.e. step through each char in a string, promoting it
        based on it's value)
        """

        # check if we need to lowercase based on the build_tree param
        tmp_item = item.name
        if self._ignore_case:
            tmp_item = item.name.lower()

        # get the ordinal position of each char
        # NB: if the key (char) is present, the get() function returns the
        # value of the specified key. if the key is not present, it returns the
        # second (ord of char in string.printable, i.e. a=0, b=1, c=2, etc.)
        # this is why we need to know about the ignore_case, since if it is
        # False, uppercase will always take precedence over lowercase (at least
        # in en_US str.printable, again YMMV)
        return [self._sort_order.get(char, ord(char)) for char in tmp_item]


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    a_start_dir = Path(__file__).parents[1] / "tests"

    cntree = CNTree(a_start_dir)
    cntree.make_tree()

    print()
    print(cntree.html)
    print()

# -)
