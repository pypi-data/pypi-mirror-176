# subprompt
Interactively change every line matching a regex in multiple files.

## Installation
Through PyPI:
```
python3.9 -m pip install subprompt
```

## Usage
```
usage: subprompt.py [-h] (-d | -r R) [-n N] REGEX FILES [FILES ...]

Modifies lines matched by a regex interactively

positional arguments:
  REGEX
  FILES

optional arguments:
  -h, --help  show this help message and exit
  -d          delete line
  -r R        replace match with expression
  -n N        size of lines preview (default=3)
```
