from pathlib import Path
import subprocess

P_DIR_PRJ = Path(__file__).parent
P_DIR_PO = P_DIR_PRJ / "i18n/po"
P_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"
S_EXT_MO = ".mo"
S_EXT_PO = ".po"
S_DOMAIN = "cnpot"

# make locale dir
P_DIR_LOCALE.mkdir(parents=True, exist_ok=True)

# get all po files
# Path("/home/user/project/po/en.po")
# Path("/home/user/project/po/es.po")
glob_po = f"**/*{S_EXT_PO}"
list_pos = list(P_DIR_PO.glob(glob_po, case_sensitive=False))

for item in list_pos:

    dir_po = P_DIR_LOCALE / item.stem / "LC_MESSAGES"
    dir_po.mkdir(parents=True, exist_ok=True)
    file_mo = dir_po / f"{S_DOMAIN}{S_EXT_MO}"

    # get initial cmd
    cmd = ["msgfmt", "-o", str(file_mo), str(item)]

    # do the final command
    subprocess.run(cmd, check=True)