import subprocess

# builtin
#--------

# which cd -> nothing
# type cd -> cd is a shell builtin

# equiv to trying to run a program named "cd" (there ain't one)
# subprocess.run(["cd"], shell=False)  # fail

# equiv to telling bash to do the "cd" command (commonly referred to as a
# "builtin")
# subprocess.run(["cd"], shell=True)  # pass

# external
#---------

# which ls -> /usr/bin/ls
# type ls -> ls is aliased to `ls --color=auto'
# equiv to typing "ls -l"
subprocess.run(["ls", "-l"], shell=False)  # pass (no color?)

# equiv to typing "bash -c 'ls' '-l'"
# subprocess.run(["ls", "-l"], shell=True)  # pass (ignores -l/no color)

# equiv to typing "ls -l"
# subprocess.run(["ls $0", "-l"], shell=False)  # fail

# equiv to typing "ls -l"
# subprocess.run(["ls $0", "-l"], shell=True)  # pass/no color
# equiv to typing "ls --color=auto -l"
# subprocess.run(["ls --color=auto $0", "-l"], shell=True)  # pass/use color
