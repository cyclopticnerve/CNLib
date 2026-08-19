""" docstring """
from pathlib import Path
import re
import subprocess

# - import gettext, write strings in code
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
S_EXT_DT = ".desktop"  # na

S_DIR_I18N = "i18n"
S_DIR_LOCALE = "locale"  #
# S_DIR_POT = ""  #
S_DIR_PO = "po"  #
S_DIR_DESK = "src"  # na
S_FILE_DESK_TMP = "template.desktop"  # na
S_TAG = "I18N"  #
S_ENCODING = "UTF-8"
# S_ERR_NO_LANG = "no lang in file: {}"

# NB: order of tags is important here (not in man!)
C_MAKE_POT = "xgettext -c{} -o {} -j {}"
C_MAKE_DESK = "msgfmt --desktop --template={} -d {} -o {}"
C_UPDATE = "msgmerge --update {} {} --backup=none"
C_MAKE_MOS = "msgfmt -o {} {}"

R_CHAR = r"(\"Content-Type:\s*text/plain;\s*charset=)(.*)(\\n\")"
R_CHAR_REP = r"\g<1>{}\g<3>"
R_LANG = r"\"Language:\s*(.*)\\n\""


def potpy(path_prj, path_src):
    """ docstring """

    # --------------------------------------------------------------------------
    # params to __init__

    p_dir_i18n = path_prj / S_DIR_I18N  #
    s_domain = path_prj.name  #
    # ver
    # auth
    # email

    l_exts = [".py", ".desktop", ".glade", ".ui"]  #

    # figure out in __init__
    p_dir_locale = p_dir_i18n / S_DIR_LOCALE  #
    p_dir_pot = p_dir_i18n  #
    p_dir_po = p_dir_i18n / S_DIR_PO  #
    p_dir_desk = path_prj / S_DIR_DESK  # na

    p_file_pot = p_dir_pot / f"{s_domain}{S_EXT_POT}"  #
    p_file_mo = f"{s_domain}{S_EXT_MO}"  #
    p_file_linguas = p_dir_po / S_FILE_LINGUAS
    p_file_desk_tmp = p_dir_desk / S_FILE_DESK_TMP  # na
    p_file_desk_out = p_dir_i18n / f"{s_domain}{S_EXT_DT}"  # na

    # --------------------------------------------------------------------------
    # defaults for file extensions (merged with list_exts)

    # --------------------------------------------------------------------------
    # housekeeping

    # nuke old pot
    if p_file_pot.exists():
        p_file_pot.unlink()

    # this is very important for -j: file must exist
    p_file_pot.parent.mkdir(parents=True, exist_ok=True)
    p_file_pot.touch(exist_ok=True)

    # make locale dir
    p_dir_locale.mkdir(parents=True, exist_ok=True)

    # make po dir
    p_dir_po.mkdir(parents=True, exist_ok=True)

    # get all po files as Paths
    glob_po = f"**/*{S_EXT_PO}"
    list_pos = list(p_dir_po.glob(glob_po, case_sensitive=False))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 1: make pot

    # get sources as space-separated string
    str_src = ""

    # for each source ext
    for ext in l_exts:
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
    cmd = C_MAKE_POT.format(S_TAG, str(p_file_pot), str_src)
    subprocess.run(cmd, shell=True, check=True)

    # --------------------------------------------------------------------------
    # fix charset

    # read in file
    with open(p_file_pot, encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # do replace
    str_pattern = R_CHAR
    str_rep = R_CHAR_REP.format(S_ENCODING)
    text = re.sub(str_pattern, str_rep, text)

    # write out file
    with open(p_file_pot, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 2: update po's from pot

    for item in list_pos:
        cmd = C_UPDATE.format(str(item), str(p_file_pot))
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
                print(f"no_lang:{item}")
                continue

        # make file structure
        dir_mo = p_dir_locale / lang / S_LC_MSG
        dir_mo.mkdir(parents=True, exist_ok=True)
        file_mo = dir_mo / p_file_mo

        # do the thing
        cmd = C_MAKE_MOS.format(str(file_mo), str(item))
        subprocess.run(cmd, shell=True, check=True)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # step 4: make desktop

    # --------------------------------------------------------------------------
    # make LINGUAS file

    # get paths for LINGUAS file
    list_pos = [item.relative_to(p_dir_po) for item in list_pos]
    list_pos = [item.with_suffix("") for item in list_pos]
    list_pos = [str(item) for item in list_pos]

    # make a space-separated string of entries
    linguas_str = " ".join(list_pos)

    # write to file
    with open(p_file_linguas, "w", encoding=S_ENCODING) as f:
        f.write(linguas_str)

    # --------------------------------------------------------------------------

    # do the thing
    cmd = C_MAKE_DESK.format(
        str(p_file_desk_tmp), str(p_dir_po), str(p_file_desk_out)
    )
    if p_file_desk_tmp.exists():
        subprocess.run(cmd, shell=True, check=True)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# do main
if __name__ == "__main__":

    P_DIR_PRJ = Path(__file__).parent
    P_DIR_SRC = P_DIR_PRJ  # / "src"
    potpy(P_DIR_PRJ, P_DIR_SRC)
