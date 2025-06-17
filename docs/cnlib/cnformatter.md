Module cnlib.cnformatter
========================
A dummy class to combine multiple argparse formatters

Classes
-------

`CNFormatter(prog, indent_increment=2, max_help_position=24, width=None)`
:   A dummy class to combine multiple argparse formatters
    
    Args:
        RawTextHelpFormatter: Maintains whitespace for all sorts of help text,
        including argument descriptions.
        RawDescriptionHelpFormatter: Indicates that description and epilog are
        already correctly formatted and should not be line-wrapped.
    
    A dummy class to combine multiple argparse formatters.

    ### Ancestors (in MRO)

    * argparse.RawTextHelpFormatter
    * argparse.RawDescriptionHelpFormatter
    * argparse.HelpFormatter