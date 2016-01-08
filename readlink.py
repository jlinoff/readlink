#!/usr/bin/env python
'''
A complete rewrite of linux readlink 8.4 in Python for Mac OSX because
I really miss "readlink -f".
'''
import os
import sys


def err(msg):
    '''
    Print an error message and exit.
    '''
    sys.stderr.write('readlink: {}\n'.format(msg))
    sys.exit(1)


def usage():
    '''
    Help.
    '''
    print('''Usage: readlink [OPTION]... FILE
Print value of a symbolic link or canonical file name

  -f, --canonicalize            canonicalize by following every symlink in
                                every component of the given name recursively;
                                all but the last component must exist
  -e, --canonicalize-existing   canonicalize by following every symlink in
                                every component of the given name recursively,
                                all components must exist
  -m, --canonicalize-missing    canonicalize by following every symlink in
                                every component of the given name recursively,
                                without requirements on components existence
  -n, --no-newline              do not output the trailing newline
  -q, --quiet,
  -s, --silent                  suppress most error messages
  -v, --verbose                 report error messages
  -h, --help                    display this help and exit
  -V, --version                 output version information and exit

WARNING! This tool is a complete rewrite of the linux version 8.4 to
         provide the same capability on Mac OSX.
         It may not behave identically in all cases.
         If you encounter problems please report them to me at:
            https://github.com/jlinoff/readlink''')
    sys.exit(0)


def version():
    '''
    Report version information and exit.
    '''
    print('''{0} 0.1.0
License: MIT
Source: https://github.com/jlinoff/readlink
The original version of this program was written by Dmitry V. Levin.'''
          .format(os.path.basename(sys.argv[0])))
    sys.exit(0)


def getopts():
    '''
    Get the command line options.
    '''
    files = []
    newline = True
    verbose = 1
    mode = ''
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg in ['-f', '--canonicalize']:
            mode = 'f'
        elif arg in ['-e', '--canonicalize-existing']:
            mode = 'e'
        elif arg in ['-m', '--canonicalize-missing']:
            mode = 'm'
        elif arg in ['-h', '--help']:
            usage()
        elif arg in ['-n', '--no-newline']:
            newline = False
        elif arg in ['-q', '--quiet', '-s', '--silent']:
            verbose = 0
        elif arg in ['-v', '--verbose']:
            verbose = 2
        elif arg in ['--version']:
            version()
        elif arg.startswith('-'):
            err("Invalid option -- '{}'".format(arg))
        else:
            # The original tool only supported one operand.
            # In the future we might want to support more.
            if len(files) > 1:
                err("Extra operand '{}'".format(arg))
            files.append(arg)
    return files, newline, verbose, mode


def main():
    '''
    Main
    '''
    files, newline, verbose, mode = getopts()

    def wr(msg):
        ''' Write a message with or without a newline. '''
        sys.stdout.write(msg)
        if newline is True:
            sys.stdout.write('\n')

    for path in files:
        if mode == '':
            # Only generate output if the file is a link.
            if os.path.islink(path):
                real = os.path.realpath(path)
                if os.path.isabs(path):
                    wr(os.path.abspath(real))
                else:
                    wr(os.path.relpath(real))
            elif verbose > 1:
                err('{}: Invalid argument'.format(path))
        elif mode == 'f':
            # All but the last must exist.
            real = os.path.realpath(path)
            full = os.path.abspath(real)
            dirname = os.path.dirname(full)
            if os.path.exists(dirname):
                wr(full)
            elif verbose > 1:
                err('{}: No such directory'.format(path))
        elif mode == 'e':
            # All components must exist.
            real = os.path.realpath(real)
            full = os.path.abspath(path)
            if os.path.exists(full):
                wr(full)
            elif verbose > 1:
                err('{}: No such file or directory'.format(path))
        elif mode == 'm':
            # It doesn't matter if any exist.
            real = os.path.realpath(real)
            wr(os.path.abspath(real))


if __name__ == '__main__':
    main()
