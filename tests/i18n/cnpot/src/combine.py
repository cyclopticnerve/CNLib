from pathlib import Path
import re
import subprocess

# ------------------------------------------------------------------------------
# params

P_DIR_PRJ = Path(__file__).parents[1]  # param
P_DIR_SRC = P_DIR_PRJ / "src"  # param

# ------------------------------------------------------------------------------
# constants

S_EXT_POT = ".pot"
S_EXT_PO = ".po"
S_EXT_MO = ".mo"
S_EXT_DT = ".desktop"
S_LC_MSG = "LC_MESSAGES"
S_FILE_LINGUAS = "LINGUAS"

# NB: order of tags is important here (not in man!)
C_MAKE_POT = "xgettext -c{} -o {} -j {}"
C_UPDATE = "msgmerge --update {} {} --backup=none"
C_MAKE_MOS = "msgfmt -o {} {}"
C_MAKE_DESK = "msgfmt --desktop --template={} -d {} -o {}"

R_CHAR = r"(\"Content-Type:\s*text/plain;\s*charset=)(.*)(\\n\")"
R_CHAR_REP = r"\g<1>{}\g<3>"
R_LANG = r"\"Language:\s*(.*)\\n\""

# ------------------------------------------------------------------------------
# constant for now

S_DOMAIN = P_DIR_PRJ.name  # TODO: do this after pass P_DIR_PRJ
S_DIR_I18N = "i18n"
S_DIR_LOCALE = "locale"
S_DIR_POT = ""
S_DIR_PO = "po"
S_DIR_DESK = "src"
S_FILE_DESK_TMP = "template.desktop"
S_TAG = "i18n"

P_DIR_I18N = P_DIR_PRJ / S_DIR_I18N
P_DIR_LOCALE = P_DIR_I18N / S_DIR_LOCALE
P_DIR_POT = P_DIR_I18N / S_DIR_POT
P_DIR_PO = P_DIR_I18N / S_DIR_PO
P_DIR_DESK = P_DIR_PRJ / S_DIR_DESK

P_FILE_POT = (
    P_DIR_POT / f"{S_DOMAIN}{S_EXT_POT}"
)  # TODO: do this after get domain
P_FILE_MO = f"{S_DOMAIN}{S_EXT_MO}"  # TODO: do this after get domain
P_FILE_LINGUAS = P_DIR_PO / S_FILE_LINGUAS
P_FILE_DESK_TMP = P_DIR_DESK / S_FILE_DESK_TMP
P_FILE_DESK_OUT = (
    P_DIR_I18N / f"{S_DOMAIN}{S_EXT_DT}"
)  # TODO: do this after get domain

L_EXTS = [".py", ".desktop", ".glade", ".ui"]

# ------------------------------------------------------------------------------
# housekeeping

# nuke old pot
if P_FILE_POT.exists():
    P_FILE_POT.unlink()

# this is very important for -j: file must exist
P_FILE_POT.parent.mkdir(parents=True, exist_ok=True)
P_FILE_POT.touch(exist_ok=True)

# make locale dir
P_DIR_LOCALE.mkdir(parents=True, exist_ok=True)

# make po dir
P_DIR_PO.mkdir(parents=True, exist_ok=True)

# get all po files
glob_po = f"**/*{S_EXT_PO}"
list_pos = list(P_DIR_PO.glob(glob_po, case_sensitive=False))

# ------------------------------------------------------------------------------
# step 1: make pot

# get sources as space-separated string
str_src = ""

# for each source ext
for ext in L_EXTS:
    glob_src = f"**/*{ext}"
    list_src = list(P_DIR_SRC.glob(glob_src, case_sensitive=False))
    list_src = [str(item) for item in list_src]
    list_src = " ".join(list_src)

    # extend source list
    str_src += f" {list_src}"

# do the thing
cmd = C_MAKE_POT.format(S_TAG, str(P_FILE_POT), str_src)
subprocess.run(cmd, shell=True, check=True)

# fix charset

# read in file
with open(P_FILE_POT, encoding="UTF-8") as a_file:
    text = a_file.read()

# do replace
str_pattern = R_CHAR
str_rep = R_CHAR_REP.format("UTF-8")
text = re.sub(str_pattern, str_rep, text)

# write out file
with open(P_FILE_POT, "w", encoding="UTF-8") as a_file:
    a_file.write(text)

# ------------------------------------------------------------------------------
# step 2: update po's from pot

for item in list_pos:
    cmd = C_UPDATE.format(str(item), str(P_FILE_POT))
    subprocess.run(cmd, shell=True, check=True)

# ------------------------------------------------------------------------------
# DO TRANSLATION HERE
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# step 3: convert po's to mo's

for item in list_pos:

    # default lang
    lang = item.stem

    # look in file
    with open(item, encoding="UTF-8") as a_file:
        text = a_file.read()

        # get lang in file
        res = re.search(R_LANG, text)
        if res:
            lang = res.group(1)

    # make file structure
    dir_mo = P_DIR_LOCALE / lang / S_LC_MSG
    dir_mo.mkdir(parents=True, exist_ok=True)
    file_mo = dir_mo / P_FILE_MO

    # do the thing
    cmd = C_MAKE_MOS.format(str(file_mo), str(item))
    subprocess.run(cmd, shell=True, check=True)

# ------------------------------------------------------------------------------
# step 4: make desktop

# get paths for LINGUAS file
list_pos = [item.relative_to(P_DIR_PO) for item in list_pos]
list_pos = [item.with_suffix("") for item in list_pos]
list_pos = [str(item) for item in list_pos]

# make a space-separated string of entries
linguas_str = " ".join(list_pos)

# write to file
with open(P_FILE_LINGUAS, "w", encoding="UTF-8") as f:
    f.write(linguas_str)

# do the thing
cmd = C_MAKE_DESK.format(
    str(P_FILE_DESK_TMP), str(P_DIR_PO), str(P_FILE_DESK_OUT)
)
if P_FILE_DESK_TMP.exists():
    subprocess.run(cmd, shell=True, check=True)
