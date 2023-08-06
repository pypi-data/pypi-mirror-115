"""
Usage:
  nnff init [--url] [<--frame-save-dir>]
  nnff (-h | --help)
  nnff (-V | --version)

Commands:
  usage             Show usages help. 
  init              Init neural network file frame.

Options:
  -h --help         Show version.
  -V --version      Show version and exit.
  --url             Url of neutral network file framwork you want to download.
  --frame-save-dir  Where you want to save.
"""

from docopt import docopt
from git.cmd import Git
import os

def main():
    args = docopt(__doc__, version="nnff 0.2.1")
    print(args)
    git = Git(os.getcwd())
    if args['init']:
        if args['--url'] != False:
            url = args['--url']
        else:
            url = 'https://github.com/lzfshub/nnfileframe.git'
        if args['<--frame-save-dir>'] != None:
            dst = args['<--frame-save-dir>']
        else:
            dst = './'
        cmd = f"git clone {url} {dst}"
        print(cmd)
        output = git.execute(cmd)
        print(output)


if __name__ == '__main__':
    main()


'''
1. python setup.py sdist bdist_wheel
2. twine upload dist/*
'''
