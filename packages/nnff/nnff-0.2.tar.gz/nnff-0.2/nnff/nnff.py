import sys
import os
class ArgumentParser(object):
    def __init__(self, argv=None):
        super(ArgumentParser, self).__init__()
        self.args = argv
        self.total_args = len(self.args)
        self.args_add_all = [] # add cmds and opts
        self.args_help_cmd = [] # add cmds help
        self.args_help_opt = [] # add opts help
        self.help = []
        self.args_p = {}
    def add_argument(self, *names, help=None, default=None):
        name_str = '  '
        total_str = 25
        if names[0][0] == '-':
            for name in names:
                name_split = name.split()[0]
                self.args_add_all.append(name_split)
                name_str += (name + ' ')
            other = ' '*(total_str-len(name_str))
            help_str = name_str + other + help
            self.args_help_opt.append(help_str + '\n')
        else:
            self.args_add_all.append(names[0])
            name_str = '  '+ names[0]
            other = ' '*(total_str-len(name_str))
            help_str = name_str + other + help
            self.args_help_cmd.append(help_str + '\n')
    
    def parse_args(self):
        cmd_args = {}
        opt_one_args = {}
        opt_two_args = {}
        num = 0
        try_ = True
        for name in self.args:
            if try_:
                if self.args[num][0] == '-' and self.args[num][1] != '-':
                    opt_one_args[name] = None
                    num += 1
                elif self.args[num][0] == '-' and self.args[num][1] == '-':
                    name = self.args[num]
                    num += 1
                    if num == self.total_args:
                        print(f"Error: You need input a param of '{self.args[num- 1]}'.")
                        sys.exit()
                    else:
                        if self.args[num][0] == '-':
                            print(f"Error: '{self.args[num]}' is not a correct param.")
                            sys.exit()
                        else:
                            value = self.args[num]
                            opt_two_args[name] = value
                            try_ = False
                            num += 1
                else:
                    cmd_args[self.args[num]] = None
                    num += 1
            else:
                try_ = True
        self.args_p = dict(cmd_args, **opt_one_args)
        self.args_p = dict(self.args_p, **opt_two_args)

        for name in self.args_p:
            if name in self.args_add_all:
                    pass
            else:
                print(f"No command or options named '{name}', please ues 'nnff -h or nnff --help' to find correct command or options.")
                sys.exit()
        return self.total_args, self.args_p

    def get_help(self):
        help_str = "\nUsage:\n  nnff <command> [options]\nCommands:\n"
        for help in self.args_help_cmd:
            help_str += help
        help_str += "Options:\n"
        for help in self.args_help_opt:
            help_str += help
        return help_str

argv = sys.argv[1:]
parser = ArgumentParser(argv=argv)
parser.add_argument('init', help="Init your neutral network file framwork.")
parser.add_argument('-h', '--help', help="Show help.")
parser.add_argument('-v', '--version', help="Show version and exit.")
parser.add_argument('--save-dir <dir>', help="The path where you want to save.")
parser.add_argument('--url <url>', help="Url of neutral network file framwork you want to download.")
total_args, args = parser.parse_args()

def main(initial_args=None):
    if initial_args is None:
        initial_args = sys.argv[1:]
    if '-h' in args or '--help' in args or total_args == 0:
        help_str = parser.get_help()
        print(help_str)
        sys.exit()
    # version
    if '-v' in args or '--version' in args or total_args == 0:
        print('nnff 0.1')
        sys.exit()
    if 'init' in args:
        if '--url' in args:
            url = args['--url']
        else:
            url = 'https://github.com/lzfshub/nnfileframe.git'
        if '--save-dir' in args:
            dst = args['--save-dir']
        else:
            dst = './'
        os.system(f"git clone {url} {dst}")



'''
pack *.py to *.exe
1. pip install pyinstaller
2. pyinstaller -F nnff.py  -i myico.ico
pack to pypi
python setup.py sdist bdist_wheel
'''