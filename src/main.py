from textnode import *
from htmlnode import *
import os
import shutil

def main():
    # path  
    src = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/static/')
    dest = os.path.expanduser('~/workspace/github.com/IvKovalenko/htmlsitegenerator/public/')
    destination = shutil.copytree(src, dest, dirs_exist_ok=True)  
    # Print path of newly created file  
    print("Destination path:", destination)
if __name__ == "__main__":
    main()