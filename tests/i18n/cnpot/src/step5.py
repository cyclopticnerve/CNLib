from pathlib import Path
import subprocess

P_DIR_PRJ = Path(__file__).parent
P_DIR_PO = P_DIR_PRJ / "i18n/po"
P_FILE_LINGUAS = P_DIR_PO / "LINGUAS"
S_EXT_PO = ".po"

P_DESK_TMP = P_DIR_PRJ / "template.desktop"
P_DESK_OUT = P_DIR_PRJ / "i18n/cnpot.desktop"

# ------------------------------------------------------------------------------

# get all po files
# Path("/home/user/project/po/en.po")
# Path("/home/user/project/po/es.po")
glob_po = f"**/*{S_EXT_PO}"
list_pos = list(P_DIR_PO.glob(glob_po, case_sensitive=False))

# strip po dir and extension from each entry and make them strings
# "es"
# "en"
list_pos = [item.relative_to(P_DIR_PO) for item in list_pos]
list_pos = [item.with_suffix("") for item in list_pos]
list_pos = [str(item) for item in list_pos]

# make a space-separated string of entries
# "en es"
linguas_str = " ".join(list_pos)
with open(P_FILE_LINGUAS, "w", encoding="UTF-8") as f:
    f.write(linguas_str)

# ------------------------------------------------------------------------------

# get initial cmd
cmd = [
    "msgfmt",
    "--desktop",
    f"--template={str(P_DESK_TMP)}",
    "-d",
    str(P_DIR_PO),
    "-o",
    str(P_DESK_OUT),
]

# do the final command
subprocess.run(cmd, check=True)
