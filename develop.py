#!/usr/bin/env python

"""fuck off"""

# 1. make venv with small name
# 2. which reqs to install?
#   pkg: only install self as editable
#   cli: install from template req
#   PP/PM/PB:
#       prj: install ???
#       inst: install ???
#   CNLib:
#       prj: install ???
#       inst: install ???
#   other prj:
#       ???

import json
from pathlib import Path
# import shlex
import subprocess
import sys

# ------------------------------------------------------------------------------

p_dir_prj = Path(__file__).parent.resolve()
p_file_prv = p_dir_prj / "pyplate/private/private.json"

# get dict prv prj
with open(p_file_prv, encoding="UTF8") as a_file:
    dict_prv = json.load(a_file)

# get inner dicts
dict_prv_all = dict_prv["PRV_ALL"]
dict_prv_prj = dict_prv["PRV_PRJ"]

# get small name
name_venv = dict_prv_prj["__PP_NAME_VENV__"]
MAKE_CMD = f"cd {p_dir_prj};python -m venv {name_venv}"

# is pkg?
is_pkg = dict_prv_prj["__PP_TYPE_PRJ__"] == "p"
PKG_CMD = (
    f"cd {p_dir_prj};. {name_venv}/bin/activate;python -m pip install -e ."
)
reqs_file = dict_prv_all["__PP_REQS_FILE__"]
CLI_CMD = f"cd {p_dir_prj};. {name_venv}/bin/activate;python -m pip install -r {reqs_file}"

# ------------------------------------------------------------------------------

# make
print("Making venv... ", end="", flush=True)

try:
    subprocess.run(MAKE_CMD, shell=True, check=True)
except FileNotFoundError as e:
    print("Failed")
    print(e.strerror)
    sys.exit()
except subprocess.CalledProcessError as e:
    print("Failed")
    print(e.stderr)
    sys.exit()

print("Done")

# what install cmd
if is_pkg:
    CMD = PKG_CMD
    print("Installing self:", flush=True)
else:
    CMD = CLI_CMD
    print("Installing requirements:", flush=True)


# do install cmd
try:
    subprocess.run(CMD, shell=True, check=True)
except FileNotFoundError as e:
    print("Failed")
    print(e.strerror)
    sys.exit()
except subprocess.CalledProcessError as e:
    print("Failed")
    print(e.stderr)
    sys.exit()

# print("Done")
