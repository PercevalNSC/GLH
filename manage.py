import sys

from manage_modules.ServerModule import server_run
from manage_modules.FigureModule import figure

def parse_option(option):
    if option == "server" :
        server_run()
    elif option == "plot" :
        figure()
    elif option == "analyze" :
        pass
    else :
        print("Undefined option.")

def parse_args(args):
    if len(args) > 0 :
        option = args[0]
        parse_option(option)
    else :
        print("too short args.")

if __name__ == "__main__" :
    args = sys.argv[1:]
    parse_args(args)