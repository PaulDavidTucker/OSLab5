#!/usr/bin/env python

"""my_run_shell_0.py:
Simple shell to start programs, e.g., try "PShell>ps" and "PShell>ls".

The purpose of this script is to give you simple functions
for locating an executable program in common locations in Linux/UNIX
(PATH environmental variable).

You are meant to paste your code from your solution in Part A
into the relevant points in this script.

Try to stick to Style Guide for Python Code and Docstring Conventions:
see https://peps.python.org/pep-0008 and https://peps.python.org/pep-0257/

(Note: The breakdown into Input/Action/Output in this script is just a suggestion.)
"""

from datetime import datetime
import os, shutil, sys

from colorama import Fore

# Here the path is hardcoded, but you can easily optionally get your PATH environ variable
# by using: path = os.environ['PATH'] and then splitting based on ':' such as the_path = path.split(':')
THE_PATH = ["/bin/", "/usr/bin/", "/usr/local/bin/", "./"]

# ========================
#   Run command
#   Run an executable somewhere on the path
#   Any number of arguments
# ========================
def runCmd(fields):
    """Returns nothing (after trying to execute user command expressed in fields).
    
    Input: takes a list of text fields (and global list of directories to search)
    Action: executes command
    Output: returns no return value
    """
    
    global THE_PATH
    cmd = fields[0]
    
    execname = add_path(cmd, THE_PATH)

    # run the executable
    if execname == None:
        print ("Executable file", cmd, "not found")
    else:
        # execute the command
        print(execname)

# execv executes a new program, replacing the current process; on success, it does not return.
# On Linux systems, the new executable is loaded into the current process, and will have the same process id as the caller.
    try:
        #creates child, if in child then os.execv, else wait for child
        pid = os.fork()

        if pid == 0:
            os.execv(execname, fields)
            os.exit(0)
        else:
            os.wait()
        
    except :
        print("Something went wrong there")
        os._exit(0)

# ========================
#   Constructs the full path used to run the external command
#   Checks to see if an executable file can be found in one of the provided directories.
#   Returns None on failure.
# ========================
def add_path(cmd, executable_dirs):
    """Returns command with full path when possible and None otherwise.
    
    Input: takes a command and a list of paths to search
    Action: no actions
    Output: returns external command prefaced by full path
            (returns None if executable file cannot be found in any of the paths)
    """
    if cmd[0] not in ['/', '.']:
        for dir in executable_dirs:
            execname = dir + cmd
            if os.path.isfile(execname) and os.access(execname, os.X_OK):
                return execname
        return None
    else:
        return cmd

# ========================
#   files command
#   List file and directory names
#   No arguments
# ========================
def filesCmd(fields):
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
#   List file information
#   1 argument: file name
# ========================
def infoCmd(fields):
    """Return nothing after printing basic file information about target file.
    
    Input: takes a list of text fields
    Action: prints our the name, owner, file/dir status, size (bytes), date of last access, date of last permissions mod, date of last
    modification and if the program can be executed or not.  
    Output: returns no return value
    """


    if checkArgs(fields, 1):
            #Assign inputted param to var
            filename = fields[1]
            try:
                #Have an OS.stat object
                Result = os.stat(filename)
                #Pull and print info
                print(Fore.BLUE + 'Name: ' + Fore.WHITE +filename)
                print(Fore.BLUE + "Owner: " +Fore.WHITE + pwd.getpwuid(Result.st_uid).pw_name)
                
                #determine dir or file type.
                if (os.path.isdir(filename)):
                    print(Fore.BLUE + "Type: " +Fore.WHITE +"Dir")
                else:
                    #Print extra info
                    print(Fore.BLUE + "Type: " +Fore.WHITE +"File")
                    print(Fore.BLUE + 'Size (Bytes): ' + Fore.WHITE + str(Result.st_size))
                    print(Fore.BLUE + 'Date of last access: ' +Fore.WHITE + datetime.fromtimestamp(os.path.getatime(filename)).strftime('%b %d %Y %H:%M:%S'))
                    print(Fore.BLUE + 'Date of last access permissions modification: ' +Fore.WHITE + datetime.fromtimestamp(os.path.getctime(filename)).strftime('%b %d %Y %H:%M:%S'))
                
                print(Fore.BLUE + 'Date of last modification: ' +Fore.WHITE + datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%b %d %Y %H:%M:%S'))
                print(Fore.BLUE + "Executable? : " +Fore.WHITE + str(os.access(os.path.abspath(filename), os.X_OK)))
            #Error handling
            except:
                print(Fore.RED + "ERROR  - No file named: "+filename + Fore.WHITE)
            

# ====================================================
#  Delete command, allows removal of file from system
#       Deletes target file, provided it exists.
#       1 Command argument: file name
#=====================================================

def deleteCmd(fields):

    """Return nothing after pdeleting the target file. If filename cannot be found, throw error
    
    Input: takes a list of text fields
    Action: deletes the targeted file and prints a success message.
    Output: returns no return value
    """


    if checkArgs(fields, 1):
        filename = fields[1]
        if os.path.exists(filename):
            os.remove(filename)
            print(Fore.BLUE + "File Removed." + Fore.WHITE)
        else:
            print(Fore.RED + "ERROR - File not found. Perhaps check your working directory?" + Fore.WHITE)


# ====================================================
#  Copy command, allows duplication of a selected file to a targeted name
#       Duplucates soruce file, provided name of dest file does not exist
#       2 Command arguments:  src file name, dest file name
#=====================================================

def copyCmd(fields):

    """Return nothing after duplicating the target file. If src filename cannot be found, throw error. if DEST already exists, throw error
    
    Input: takes a list of text fields
    Action: duplicates a target into filename of DEST
    Output: returns no return value
    """

    if checkArgs(fields, 2):
        fromFile = fields[1]
        toFile = fields[2]
        if os.path.exists(fromFile) and not os.path.exists(toFile):
            shutil.copyfile(fromFile, toFile)
            print(Fore.BLUE + "File Copied successfully. " + Fore.WHITE)
        else:
            print(Fore.RED + "Error - Source file either does not exist or destination file already exists." + Fore.WHITE)



# ====================================================
#  Where command,  prints name of current working directory
#       
#       0 Command arguments.
#=====================================================

def whereCmd(feilds):

    """Return nothing after printing the name of the current working dir as a string to console
    
    Input: takes a list of text fields
    Action: Prints current working dir to console
    Output: returns no return value
    """


    if checkArgs(feilds, 0):
        print(os.getcwd())


def downCmd(fields):

    """Return nothing after mocing into target sub diretory
    
    Input: takes a list of text fields
    Action: Move into target sub directory 
    Output: returns no return value
    """

    if checkArgs(fields, 1):
        if os.path.exists(fields[1]):
            try:
                currentDir = os.getcwd()
                os.chdir(currentDir +"/" +fields[1])
            except:
                print(Fore.RED + "ERROR" + Fore.WHITE)

        else:
            print(Fore.RED + "ERROR - Directory not found" + Fore.WHITE)

# ====================================================
#  Up command, moves up the working dir tree
#       0 commands
#=====================================================

def upCmd(fields):

    """Return nothing after moving up the working tree
    
    Input: takes a list of text fields
    Action: move up tree
    Output: returns no return value
    """

    if checkArgs(fields, 0):
        try:
            if not os.getcwd() == "/":
                os.chdir("..")
            else:
                print(Fore.RED + "ERROR -AT HOME DIRECTORY, CANNOT STEP BACK" + Fore.WHITE)
        except:
            print(Fore.RED + "ERROR - CANNOT STEP BACK" + Fore.WHITE)


# ====================================================
#  Exit command, Quit the shell
#       0 commands
#=====================================================

def exitCmd(fields):

    """Return nothing after exiting the shell

    Input: takes a list of text fields
    Action: Exit the shell
    Output: returns no return value
    """

    if checkArgs(fields, 0):
        print(Fore.GREEN + "Goodbye..")
        sys.exit()



# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
    """Returns if len(fields)-1 == num (prints error to shell if not).
    
    Input: takes a list of text fields and how many non-command fields are expected
    Action: prints an error message if the number of fields is unexpected
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
    
        if fields[0] == "files":
            filesCmd(fields)
        elif fields[0] == "info":
            infoCmd(fields)
        elif fields[0] == "delete":
            deleteCmd(fields)
        elif fields[0] == "copy":
            copyCmd(fields)
        elif fields[0] == "where":
            whereCmd(fields)
        elif fields[0] == "down":
            downCmd(fields)
        elif fields[0] == "up":
            upCmd(fields)
        elif fields[0] == "exit":
            exitCmd(fields)
        else:
            runCmd(fields)
    
    return 0 # currently unreachable code

if __name__ == '__main__':
    sys.exit(main()) # run main function and then exit
