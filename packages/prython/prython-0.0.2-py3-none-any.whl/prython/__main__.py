# __main__.py is the script's entrypoint, python -m <modulename> will run this file.
import prython

def main():
    explanatory_string = "PRYTHON VERSION " + prython.__version__ + """
    This package is a runtime microdebugger and cannot be executed standalone from the command line.
    
    See the docs: 
    """ + prython.__main_repo_url__
    print(explanatory_string)

if (__name__ == "main"):
    main()