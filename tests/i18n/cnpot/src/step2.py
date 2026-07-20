from pathlib import Path
import subprocess

P_DIR_PRJ = Path(__file__).parent
# output
FILE_POT = P_DIR_PRJ / "i18n/cnpot.pot"
# input
FILES_SRC = [P_DIR_PRJ / "step1.py", P_DIR_PRJ / "template.desktop"]

# nuke old pot
if FILE_POT.exists():
    FILE_POT.unlink()

# this is very important for -j: file must exist
FILE_POT.parent.mkdir(parents=True, exist_ok=True)
FILE_POT.touch(exist_ok=True)

# do the final command
for item in FILES_SRC:
    cmd = ["xgettext", "-o", str(FILE_POT), str(item), "-j", "-cI18N"]

    # do the final command
    subprocess.run(cmd, check=True)
