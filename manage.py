import sys

from manage_modules.ServerModule import server_run
from manage_modules.FigureModule import figure
from manage_modules.LoadModule import store_GLH
from manage_modules.ClusteringModule import clustering_and_store_reachability

def parse_option(option):
    if option == "server" :
        server_run()
    elif option == "plot" :
        figure()
    elif option == "store" :
        store_GLH()
    elif option == "init_clustering":
        clustering_and_store_reachability()
    elif option == "load":
        store_GLH()
        clustering_and_store_reachability()
    elif option == "analyze" :
        print("no defined function.")
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