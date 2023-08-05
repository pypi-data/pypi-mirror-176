import os

def filePath(fileName):
    return f"oa_water_jug/src/{fileName}"

def display():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    with open(filePath('code.py')) as f:
        print("===================Water Jug====================")
        for line in f:
            print(line, end='')
display()