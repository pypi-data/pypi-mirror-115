# clname
```
usage: clname [OPTION]... FILE...

Clean the name(s) of the FILE(s) to make them shell-friendly
(i.e., get rid of characters for which escape characters `\` are necessary.)

optional arguments:
  -h, --help         show this help message and exit
  -e, --extension    also clean the file extension
  -f, --force        do not prompt before overwriting files
  -L, --dereference  follow symbolic links
  -i, --interactive  prompt before renaming 
  -r, --recursive    rename subdirectories and their contents recursively
  -s, --simulate     show what would be done without renaming anything
  -v, --verbose      explain what is being done
  --version          show copyright and version info and exit
```
## Example
```
$ ls
'[2021-07-07] - this is a  test    .txt'
$ clname \[2021-07-07\]\ -\ this\ is\ a\ \ test\ \ \ \ .txt
$ ls
2021-07-07_-_this_is_a_test.txt
```
## Requirements
* Python 3
* clname is written for GNU/Linux distributions.
## Installation
```
pip install clname
```