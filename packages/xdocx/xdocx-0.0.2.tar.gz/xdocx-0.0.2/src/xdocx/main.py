import argparse
from . import gen_report


class commandline_parse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog = 'xdocx')
        self.subparsers = self.parser.add_subparsers(title='Commands', dest='command')

        self.add_command('gen_report', gen_report.add_arguments, gen_report.run,
                        help_msg='standard genarate fw bin file')

    def add_command(self, name, add_arguments_func, run_func, help_msg, aliases=None):
        p = self.subparsers.add_parser(name, help=help_msg)
        add_arguments_func(p)
        p.set_defaults(run_func=run_func)

    def run(self):
        parser = self.parser
        options = parser.parse_args()    
        if options.command == None:
            print('please use "-h" to get help info.')
            return
        options.run_func(options)



def main():
    commandline_parse().run()


if __name__ == "__main__":
    main()