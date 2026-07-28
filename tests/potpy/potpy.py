from pathlib import Path
import re
import subprocess

# - import gettext/make _/write strings in code
# 1. make pot
# 2. update po's from pot
# -. translate po's (send file out, get file back)
# 3. convert po's to mo's
# 4. make desktop

# rinse, repeat when adding new strings or langs

# ------------------------------------------------------------------------------
# constants

S_LC_MSG = "LC_MESSAGES"
S_FILE_LINGUAS = "LINGUAS"
S_EXT_POT = ".pot"
S_EXT_PO = ".po"
S_EXT_MO = ".mo"
# S_EXT_DT = ".desktop" # na

S_DIR_I18N = "i18n"
S_DIR_LOCALE = "locale"  #
# S_DIR_POT = ""  #
S_DIR_PO = "po"  #
# S_DIR_DESK = "src"  # na
# S_FILE_DESK_TMP = "template.desktop"  # na

# S_ERR_NO_LANG = "no lang in file: {}"

# NB: order of tags is important here (not in man!)
C_MAKE_POT = "xgettext -c{} -o {} -j {}"
C_UPDATE = "msgmerge --update {} {} --backup=none"
C_MAKE_MOS = "msgfmt -o {} {}"
C_MAKE_DESK = "msgfmt --desktop --template={} -d {} -o {}"

R_CHAR = r"(\"Content-Type:\s*text/plain;\s*charset=)(.*)(\\n\")"
R_CHAR_REP = r"\g<1>{}\g<3>"
R_LANG = r"\"Language:\s*(.*)\\n\""


def potpy(path_prj, path_src):

    # --------------------------------------------------------------------------
    # params to __init__

    P_DIR_I18N = path_prj / S_DIR_I18N  #
    S_DOMAIN = path_prj.name  #
    # ver
    # auth
    # email
    S_TAG = "I18N"  #
    S_ENCODING = "UTF-8"
    L_EXTS = [".py", ".desktop", ".glade", ".ui"]  #

    # figure out in __init__
    P_DIR_LOCALE = P_DIR_I18N / S_DIR_LOCALE  #
    P_DIR_POT = P_DIR_I18N  #
    P_DIR_PO = P_DIR_I18N / S_DIR_PO  #
    # P_DIR_DESK = path_prj / S_DIR_DESK  # na

    P_FILE_POT = P_DIR_POT / f"{S_DOMAIN}{S_EXT_POT}"  #
    P_FILE_MO = f"{S_DOMAIN}{S_EXT_MO}"  #
    P_FILE_LINGUAS = P_DIR_PO / S_FILE_LINGUAS  #
    # P_FILE_DESK_TMP = P_DIR_DESK / S_FILE_DESK_TMP  # na
    # P_FILE_DESK_OUT = P_DIR_I18N / f"{S_DOMAIN}{S_EXT_DT}"  # na

    # --------------------------------------------------------------------------
    # defaults for file extensions (merged with list_exts)

    # --------------------------------------------------------------------------
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

    # get all po files as Paths
    glob_po = f"**/*{S_EXT_PO}"
    list_pos = list(P_DIR_PO.glob(glob_po, case_sensitive=False))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 1: make pot

    # get sources as space-separated string
    str_src = ""

    # for each source ext
    for ext in L_EXTS:
        glob_src = f"**/*{ext}"
        list_src = list(path_src.glob(glob_src, case_sensitive=False))
        list_src = [str(item) for item in list_src]
        list_src = " ".join(list_src)

        # extend source list
        str_src += f" {list_src}"

    # strip leading/trailing whitespace
    str_src = str_src.strip()

    # --------------------------------------------------------------------------

    # do the thing
    cmd = C_MAKE_POT.format(S_TAG, str(P_FILE_POT), str_src)
    subprocess.run(cmd, shell=True, check=True)

    # --------------------------------------------------------------------------
    # fix charset

    # read in file
    with open(P_FILE_POT, encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # do replace
    str_pattern = R_CHAR
    str_rep = R_CHAR_REP.format(S_ENCODING)
    text = re.sub(str_pattern, str_rep, text)

    # write out file
    with open(P_FILE_POT, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 2: update po's from pot

    for item in list_pos:
        cmd = C_UPDATE.format(str(item), str(P_FILE_POT))
        subprocess.run(cmd, shell=True, check=True)

    # --------------------------------------------------------------------------
    # DO TRANSLATION HERE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 3: convert po's to mo's

    for item in list_pos:

        # default lang
        lang = item.stem

        # look in file
        with open(item, encoding=S_ENCODING) as a_file:
            text = a_file.read()

            # get lang in file
            res = re.search(R_LANG, text)
            if res:
                lang = res.group(1)
            else:
                print("no_lang:{}".format(item))
                continue

        # make file structure
        dir_mo = P_DIR_LOCALE / lang / S_LC_MSG
        dir_mo.mkdir(parents=True, exist_ok=True)
        file_mo = dir_mo / P_FILE_MO

        # do the thing
        cmd = C_MAKE_MOS.format(str(file_mo), str(item))
        subprocess.run(cmd, shell=True, check=True)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 4: make desktop

    # --------------------------------------------------------------------------
    # make LINGUAS file

    # get paths for LINGUAS file
    list_pos = [item.relative_to(P_DIR_PO) for item in list_pos]
    list_pos = [item.with_suffix("") for item in list_pos]
    list_pos = [str(item) for item in list_pos]

    # make a space-separated string of entries
    linguas_str = " ".join(list_pos)

    # write to file
    with open(P_FILE_LINGUAS, "w", encoding=S_ENCODING) as f:
        f.write(linguas_str)

    # --------------------------------------------------------------------------

    # do the thing
    cmd = C_MAKE_DESK.format(
        str(P_FILE_DESK_TMP), str(P_DIR_PO), str(P_FILE_DESK_OUT)
    )
    if P_FILE_DESK_TMP.exists():
        subprocess.run(cmd, shell=True, check=True)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# do main
if __name__ == "__main__":

    P_DIR_PRJ = Path(__file__).parent
    P_DIR_SRC = P_DIR_PRJ / "src"
    potpy(P_DIR_PRJ, P_DIR_SRC)
