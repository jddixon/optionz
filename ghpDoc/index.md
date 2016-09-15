<h1 class="libTop">optionz</h1>

**Optionz** is a package for converting a series of command line arguments
into  an immutable Python data structure.  That is, it plays the same role
as C's **getopt** or the Python **argparse**.

## Command Line

As the term is used here, the command line is an array of strings,
**arguments**, as we see in `sys.argv`.  This sequence is made available to
the executing program by the
operating system.  The first element, `sys.argv[0]`, is normally the name
of the executing program.  The rest are produced by splitting the command
line into words, with any sequence of one or more delimiters used to separate
the words, except that singly- and double-quoted strings are untouched.
So the command

    abc   def  "ghi   jkl " mno

becomes the string array

    abc
    def
    ghi   jkl
    mno

## Options

A command line **option** consists of a ***tag** (usually the option name)
preceded by one or two
dashes (minus signs, `-`) and followed by zero or more **values**.  Options
and values are all simple strings.

As an example

    progName -f -b 52 --feelingGood

consists of the progran name `progName` followed by two short-form options
(`-f` and `-b`) and one long-form option (`feelingGood`).  Two of the
otions are not followed by a value and so would probably be booleans.  The
third, `-b`, has a value, `52`, which would probably be interpreted as
an integer.

### Option Names

A valid option or tag name is a sequence of printing characters, none of
which is
a delimiter (a space or a tab character).  For our immediate purposes, a
valid name matches the regular expression

    [a-zA-Z0-9_]+

This implies that any valid Python name is a valid option name, but the
opposite need not be true.  So all of these are valid option names:

    a_b  _  12  b52

but none of these is

    -5        # contains a dash
    abc.def   # contains a dot

### Short-form Options

On the command line, a short-form operation is generally
represented as single characters **tag** preceded by a
dash.  The single character may be the name of the option.
So '-f' is the short-form representation of the option `f` on the
command line.  Generally a longer option name is associated with
the single character tag represenging it on the command line.

### Long-form Options

Long-form options are represented on the command line as a tag,
a string of non-delimiting characters, preceded by a double dash (`--`).
The tag is generally the same as the option name.

## Requirements

### Tags and Option Names

**optionz** must support both long and short option forms.  The tag
in the short form must be a single character.  The tag is the long
form option can be any valid name and by default will be the option
name. One-character tags must be uniquely associated with an option
name.  That is, in a set of options, each single-character tag
corresponds to one and only one option and any option name may be
associated with one and only one single-character tog.  Similarly
options are uniquely associated with multi-character tags.  However,
and this is the more common case, any option may be associated with
both a single-character tag and a multi-character tag, and the
multi-character tag is normally identical to the option name.

## Values

Each option is associated with zero, one, or more values.  These are
represented as strings, but the `optionz` declaration will include
syntax mapping any value or values associated with an option into either a
basic data type or a collection of such.  That is, `optionz` will
automatically cast the string into a Python value of the correct type.

### Basic Data Types

These are

* integer
* float
* string
* boolean
* choices

### Collections

A **collection** in the sense in which the term is used here is a sequence
of values.  In Python terms the `optionz` deliverable corresponding to a
collection is a named tuple whose cardinality is symbolized by

* '?' zero or one values
* '\*' zero or more values
* '+' one or more values

All values in a collection are of the same basic type.

## Subcommands

`optionz` must support **subcommands**, where a subcommand is essentially
a tag followed by a nested set of options.

Where subcommands are used, the first string in the argument vector
`sys.argv` will be the program name as usual.  This may be followed
by some number of options (each consisting of one or two dashes
followed by a tag and then zero or more values) and then one of
the subcommands, each of which has the same form: the subcommand
name followed by zero or options.

## Help Messages

All `optionz` objects have a built-in **help** option which has a
`-h` short form and a `--help` long form.  These map into a single
field, which is a boolean.

## Project Status

Pre-alpha.

