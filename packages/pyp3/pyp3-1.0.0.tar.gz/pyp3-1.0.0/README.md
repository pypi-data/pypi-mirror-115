# pyp3

A minified [pyp](https://code.google.com/archive/p/pyp/) compatible with python3

Pyp is a linux command line text manipulation tool similar to awk or sed, but which uses standard python string and list methods as well as custom functions evolved to generate fast results in an intense production environment.

## Installation

### From PyPI

```sh
pip3 install pyp3
```

### From GitHub

```sh
pip3 install git+https://github.com/donno2048/pyp3
```

## Usage

Because pyp employs it's own internal piping syntax ("|") similar to unix pipes, complex operations can be proceduralized by feeding the output of one python command to the input of the next.

This greatly simplifies the generation and troubleshooting of multistep operations without the use of temporary variables or nested parentheses. The variable "p" represents each line as a string, while "pp" is entire input as python list

### Use it directly

```sh
ls | pyp3 "p[0] | pp.sort()" #gives sorted list of first letters of every line
```

## Use it as a python module

```sh
ls | python3 -m pyp3 "p.replace('.', ',')" #replaces . with ,
```
