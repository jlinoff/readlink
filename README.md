# readlink
Python port of readlink with the -f option for use on Mac OS X.

This is a complete rewrite of the linux version of readlink-8.4 in Python because I really missed the `-f` and `-m` options. It has a `.py` extension to distinguish it from the BSD version of readlink that is shipped by default.

It is very simple to use. Here are some examples.

```bash
$ ln -s readlink.py foobar
$ ./readlink.py foobar
readlink.py
$ ./readlink.py -f foobar
/Users/jlinoff/work/readlink/readlink.py
$ readlink -f readlink.py
$ ./readlink.py -f readlink.py
/Users/jlinoff/work/readlink/readlink.py
$ ./readlink.py -f wombat
$ ./readlink.py -m wombat
/Users/jlinoff/work/readlink/wombat
```

Here is how you install it.

```bash
$ [ ~/work ] && mkdir -p ~/work
$ cd work
$ git clone https://github.com/jlinoff/readlink.git
$ cp readlink/readlink.py ~/bin
$ chmod a+rwx ~/bin/readlink.py
$ # Add ~/bin to your PATH.
```

Please report any bugs to me here.
