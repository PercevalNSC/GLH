import sys

from manage_modules.ServerModule import server_run
from manage_modules.FigureModule import figure
from manage_modules.LoadModule import store, init_clustering

def parse_option(option):
    if option == "server" :
        server_run()
    elif option == "plot" :
        figure()
    elif option == "store" :
        store()
    elif option == "init_clustering":
        init_clustering()
    elif option == "load":
        store()
        init_clustering()
    elif option == "analyze" :
        pass
    elif option == "help" or option == "h" or option == "all":
        print("python manage.py server: run flask server")
        print("                 plot  : plot optics data by matplotlib")
        print("                 store : store glh json data to mongodb")
        print("                 init_clustering: init optics clustering")
        print("                 load  : store and init_clustering")
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