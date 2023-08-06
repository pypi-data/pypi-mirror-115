# __main__.py is the script's entrypoint, python -m <modulename> will run this file.
from .. import constants

def main():
    explanatory_string = """
    This package is a runtime microdebugger and cannot be executed standalone from the command line.
    
    See the docs: 
    """ + constants.GITHUB_REPO_URL
    print(explanatory_string)

if (__name__ == "main"):
    main()