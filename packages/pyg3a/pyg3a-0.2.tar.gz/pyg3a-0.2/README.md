# Description

A tool to convert Python files to Casio fx-CG 10/20/50 (Prizm) Add-ins

# Installation

    pip install pyg3a


# Usage

    pyg3a <file.py> -l path/to/libfxcg [--debug] [--verbose]


# How it works

1.  Project is Created:
    
    PyG3A will create a 'project' in the directory '`.pyg3a_build/<file>/`'. <br/>
    It then creates a Makefile to build the project later. <br/>
    This should only happen once.

2.  Python is Parsed:
    
    PyG3A uses the *libcst* module to parse the input python file.

3.  Imports are Checked:
    
    It iterates over the imports in the file, and checks the '`<install location>/packages`' and '`~/.local/lib/pyg3a/`' directory for .py files matching this name. <br/>
    The functions in this file are added to a list for future use.

4.  Code is Transpiled:
    
	PyG3A internally puts your whole Python file into the main() function, then transpiles to C++, placing function definitions outside the main() function (as C++ does not support nested functions)<br/>
    This takes into account the packages imported in your program for function overloads.

5.  C++ is Compiled:
    
    The C++ is compiled and linked using GNU Make. <br/>
    Execution starts from your Python file's main() function (if defined), or from your first statement. <br/>
    Any G++ output will be shown in the python output as a means of debugging. <br/>
    Using '`--verbose`' will print the commands that are being run through make.


# Notes

The function `raw_c(str)` inserts that str into the transpiled C++.

Importing replaces .s with /s, for example:

    import custom.random
    from custom.random import *
    from custom.random import a

All of these import the '`random`' module in the '`~/.local/lib/pyg3a/custom`' folder. <br/>
Variables are statically typed, so their type must be declared when first used.

# Syntax

| Keyword | Support | Explanation |
| ------- | ------- | ----------- |
| def | Supported |
| return | Supported |
| = | Supported |
| := | Supported |
| (operator)= | Supported |
| tuple unpacking | Supported |
| while | Supported |
| for | Supported |
| if | Supported |
| elif | Supported |
| else | Supported |
| import | Supported |
| from | Supported |
| pass | Supported |
| break | Supported |
| continue | Supported |
| lambda | Supported |
| a if b else c | Supported |
| {set} | Supported |
| a.b | Supported |
| (tuple) | Supported |
| [list] | Supported |
| and | Supported |
| or | Supported |
| + | Supported |
| - | Supported |
| \* | Supported |
| / | Supported |
| // | Supported |
| % | Supported |
| \*\* | Supported |
| << | Supported |
| >> | Supported |
| \| | Supported |
| ^ | Supported |
| & | Supported |
| ~ | Supported |
| not | Supported |
| + | Supported |
| - | Supported |
| == | Supported |
| < | Supported |
| <= | Supported |
| > | Supported |
| \>= | Supported |
| is | Supported |
| is not | Supported |
| del | Supported |
| match | Supported |
| class | Support Planned |
| f&ldquo;strings&rdquo; | Support Planned |
| [sli:ces] | Support Planned |
| list comprehension | Support Planned |
| @decorator  | Support Planned |
| async | No Support | no async support in c++ |
| await | No Support | no async support in c++ |
| with | No Support | no error support in libfxcg |
| raise | No Support | no error support in libfxcg |
| assert | No Support | no error support in libfxcg |
| try/except/else/finally | No Support | no error support in libfxcg |
| global | No Support | automatically used in c++ |
| nonlocal | No Support | no nested function support in c++ |
| dict | No Support | would be annoying to write |
| yield | No Support | no generator support in c++ |
| matrix @ matrix | No Support | little use case |
