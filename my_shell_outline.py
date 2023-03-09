#!/usr/bin/env python

"""my_shell_outline.py:
Simple shell that interacts with the filesystem, e.g., try "PShell>files".

Try to stick to Style Guide for Python Code and Docstring Conventions:
see https://peps.python.org/pep-0008 and https://peps.python.org/pep-0257/

(Note: The breakdown into Input/Action/Output in this script is just a suggestion.)
"""

from datetime import datetime
import glob
import os
import pwd
import shutil
import sys
import time
import glob
import colorama
from colorama import Fore

# ========================
#    files command
#    List file and directory names
#    No command arguments
# ========================
def files_cmd(fields):
    """Return nothing after printing names/types of files/dirs in working directory.
    
    Input: takes a list of text fields
    Action: prints for each file/dir in current working directory their type and name
            (unless list is non-empty in which case an error message is printed)
    Output: returns no return value
    """
    
    if checkArgs(fields, 0):
        for filename in os.listdir('.'):
            if os.path.isdir(os.path.abspath(filename)):
                print("dir:", filename)
            else:
                print("file:", filename)

# ========================
#  info command
#     List file information
#     1 command argument: file name
# ========================
def info_cmd(fields):
    if checkArgs(fields, 1):
            filename = fields[1]
            try:
                Result = os.stat(filename)
                print(Fore.BLUE + 'Name: ' + Fore.WHITE +filename)
                print(Fore.BLUE + "Owner: " +Fore.WHITE + pwd.getpwuid(Result.st_uid).pw_name)
                if (os.path.isdir(filename)):
                    print(Fore.BLUE + "Type: " +Fore.WHITE +"Dir")
                else:
                    print(Fore.BLUE + "Type: " +Fore.WHITE +"File")
                    print(Fore.BLUE + 'Size (Bytes): ' + Fore.WHITE + str(Result.st_size))
                    print(Fore.BLUE + 'Date of last access: ' +Fore.WHITE + datetime.fromtimestamp(os.path.getatime(filename)).strftime('%b %d %Y %H:%M:%S'))
                    print(Fore.BLUE + 'Date of last access permissions modification: ' +Fore.WHITE + datetime.fromtimestamp(os.path.getctime(filename)).strftime('%b %d %Y %H:%M:%S'))
                
                print(Fore.BLUE + 'Date of last modification: ' +Fore.WHITE + datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%b %d %Y %H:%M:%S'))
                print(Fore.BLUE + "Executable? : " +Fore.WHITE + str(os.access(os.path.abspath(filename), os.X_OK)))
            except:
                print(Fore.RED + "ERROR  - No file named: "+filename + Fore.WHITE)
                
            


# =========================
#  Delete command, allows removal of file from system
#       Deletes target file, provided it exists.
#       1 Command argument: file name
def delete_cmd(fields):
    if checkArgs(fields, 1):
        filename = fields[1]
        if os.path.exists(filename):
            os.remove(filename)
            print(Fore.BLUE + "File Removed." + Fore.WHITE)
        else:
            print(Fore.RED + "ERROR - File not found. Perhaps check your working directory?" + Fore.WHITE)


def copy_cmd(fields):
    if checkArgs(fields, 2):
        fromFile = fields[1]
        toFile = fields[2]
        if os.path.exists(fromFile) and not os.path.exists(toFile):
            shutil.copyfile(fromFile, toFile)
            print(Fore.BLUE + "File Copied successfully. " + Fore.WHITE)
        else:
            print(Fore.RED + "Error - Source file either does not exist or destination file already exists." + Fore.WHITE)

def where_cmd(feilds):
    if checkArgs(feilds, 0):
        print(os.getcwd())

def down_cmd(fields):
    if checkArgs(fields, 1):
        if os.path.exists(fields[1]):
            try:
                currentDir = os.getcwd()
                os.chdir(currentDir +"/" +fields[1])
            except:
                print(Fore.RED + "ERROR" + Fore.WHITE)

        else:
            print(Fore.RED + "ERROR - Directory not found" + Fore.WHITE)
        


def up_cmd(fields):
    if checkArgs(fields, 0):
        try:
            os.chdir("..")
        except:
            print(Fore.RED + "ERROR - CANNOT STEP BACK" + Fore.WHITE)

def exit_cmd(fields):
    if checkArgs(fields, 0):
        print(Fore.GREEN + "Goodbye..")
        sys.exit()

# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
    """Returns if len(fields)-1 == num and print an error in shell if not.
    
    Input: takes a list of text fields and how many non-command fields are expected
    Action: prints error to shell if the number of fields is unexpected
    Output: returns boolean value to indicate if it was expected number of fields
    """

    numArgs = len(fields) - 1
    if numArgs == num:
        return True
    if numArgs > num:
        print("Unexpected argument", fields[num+1], "for command", fields[0])
    else:
        print("Missing argument for command", fields[0])
        
    return False

# ---------------------------------------------------------------------

def main():
    """Returns exit code 0 (after executing the main part of this script).
    
    Input: no function arguments
    Action: run multiple user-inputted commands
    Output: return zero to indicate regular termination
    """
    
    while True:
        line = input("PShell>")
        fields = line.split()
        # split the command into fields stored in the fields list
        # fields[0] is the command name and anything that follows (if it follows) is an argument to the command
        
        if fields[0] == "files":
            files_cmd(fields)
        elif fields[0] == "info":
            info_cmd(fields)
        elif fields[0] == "delete":
            delete_cmd(fields)
        elif fields[0] == "copy":
            copy_cmd(fields)
        elif fields[0] == "where":
            where_cmd(fields)
        elif fields[0] == "down":
            down_cmd(fields)
        elif fields[0] == "up":
            up_cmd(fields)
        elif fields[0] == "exit":
            exit_cmd(fields)
        else:
            print("Unknown command", fields[0])
    
    return 0 # currently unreachable code

if __name__ == '__main__':
    sys.exit( main() ) # run main function and then exit
