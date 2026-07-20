from pathlib import Path
import subprocess

P_DIR_PRJ = Path(__file__).parent
P_DIR_PO = P_DIR_PRJ / "i18n/po"
S_EXT_PO = ".po"
FILE_POT = P_DIR_PRJ / "i18n/cnpot.pot"

# make po dir
P_DIR_PO.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------

# get all po files
# Path("/home/user/project/po/en.po")
# Path("/home/user/project/po/es.po")
glob_po = f"**/*{S_EXT_PO}"
list_pos = list(P_DIR_PO.glob(glob_po, case_sensitive=False))

# for each wlang in the po folder
for item in list_pos:

    # update existing po file using latest pot
    cmd = ["msgmerge", "--update", str(item), str(FILE_POT), "--backup=none"]

    # do the final command
    subprocess.run(cmd, check=True)
